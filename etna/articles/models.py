from typing import Any, Dict, Tuple

from django.conf import settings
from django.db import models
from django.http import HttpRequest
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from taggit.models import ItemBase, TagBase

from etna.collections.models import TopicalPageMixin
from etna.core.models import (
    BasePageWithIntro,
    ContentWarningMixin,
    HeroImageMixin,
    NewLabelMixin,
)
from etna.core.utils import skos_id_from_text
from etna.records.fields import RecordField

from .blocks import (
    ArticlePageStreamBlock,
    AuthorPromotedPagesBlock,
    FeaturedCollectionBlock,
)


class ArticleIndexPage(BasePageWithIntro):
    """ArticleIndexPage

    This page lists the ArticlePage objects that are children of this page.
    """

    featured_article = models.ForeignKey(
        "articles.ArticlePage", blank=True, null=True, on_delete=models.SET_NULL
    )
    featured_pages = StreamField(
        [("featuredpages", FeaturedCollectionBlock())],
        blank=True,
        null=True,
        use_json_field=True,
    )

    # DataLayerMixin overrides
    gtm_content_group = "stories"

    class Meta:
        verbose_name = _("article index page")

    def get_context(self, request):
        context = super().get_context(request)
        context["article_pages"] = self.get_children().public().live().specific()
        return context

    content_panels = BasePageWithIntro.content_panels + [
        FieldPanel("featured_article", heading=_("Featured article")),
        FieldPanel("featured_pages"),
    ]

    subpage_types = ["articles.ArticlePage"]


@register_snippet
class ArticleTag(TagBase):
    free_tagging = False
    skos_id = models.CharField(
        blank=True,
        unique=True,
        db_index=True,
        max_length=100,
        verbose_name="SKOS identifier",
        help_text="Used as the identifier for this tag when sending page metatdata to the CIIM API.",
    )

    class Meta:
        verbose_name = "article tag"
        verbose_name_plural = "article tags"

    panels = (
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("skos_id"),
    )

    def clean(self, *args, **kwargs):
        if not self.skos_id and self.name:
            # Generate a unique skos_id value for new tags
            base_value = skos_id_from_text(self.name)
            self.skos_id = base_value
            i = 2
            while (
                ArticleTag.objects.exclude(id=self.id)
                .filter(skos_id=self.skos_id)
                .exists()
            ):
                self.skos_id = f"{base_value[:97]}_{i}"
                i += 1
        return super().clean(*args, **kwargs)


class TaggedArticle(ItemBase):
    tag = models.ForeignKey(
        ArticleTag, related_name="tagged_article", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to="articles.ArticlePage",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )


class ArticlePage(
    TopicalPageMixin,
    HeroImageMixin,
    ContentWarningMixin,
    NewLabelMixin,
    BasePageWithIntro,
):
    """ArticlePage

    The ArticlePage model.
    """

    body = StreamField(
        ArticlePageStreamBlock, blank=True, null=True, use_json_field=True
    )
    article_tag_names = models.TextField(editable=False)
    tags = ClusterTaggableManager(through=TaggedArticle, blank=True)

    search_fields = BasePageWithIntro.search_fields + [
        index.AutocompleteField("article_tag_names"),
    ]

    # DataLayerMixin overrides
    gtm_content_group = "stories"

    template = "articles/article_page.html"

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    content_panels = (
        BasePageWithIntro.content_panels
        + HeroImageMixin.content_panels
        + [
            FieldPanel("tags"),
            MultiFieldPanel(
                [
                    FieldPanel("display_content_warning"),
                    FieldPanel("custom_warning_text"),
                ],
                heading="Content Warning Options",
                classname="collapsible",
            ),
            FieldPanel("body"),
        ]
    )

    promote_panels = (
        NewLabelMixin.promote_panels
        + BasePageWithIntro.promote_panels
        + [
            TopicalPageMixin.get_topics_inlinepanel(),
            TopicalPageMixin.get_time_periods_inlinepanel(),
        ]
    )

    parent_page_types = ["articles.ArticleIndexPage"]
    subpage_types = []

    search_fields = BasePageWithIntro.search_fields + [
        index.AutocompleteField("body"),
        index.AutocompleteField("article_tag_names", boost=2),
        index.AutocompleteField("topic_names", boost=1),
        index.AutocompleteField("time_period_names", boost=1),
    ]

    def get_datalayer_data(self, request: HttpRequest) -> Dict[str, Any]:
        data = super().get_datalayer_data(request)
        data.update(
            customDimension4="; ".join(obj.title for obj in self.topics),
            customDimension6="; ".join(self.article_tag_names.split("\n")),
            customDimension7="; ".join(obj.title for obj in self.time_periods),
        )
        return data

    def save(self, *args, **kwargs):
        """
        Overrides Page.save() to ensure 'article_tag_names' always reflects the tags() value
        """
        if (
            "update_fields" not in kwargs
            or "article_tag_names" in kwargs["update_fields"]
        ):
            self.article_tag_names = "\n".join(t.name for t in self.tags.all())
        super().save(*args, **kwargs)

    @cached_property
    def similar_items(self) -> Tuple["ArticlePage"]:
        """
        Returns a maximum of three ArticlePages that are tagged with at least
        one of the same ArticleTags. Items should be ordered by the number
        of tags they have in common.
        """
        if not self.article_tag_names:
            # Avoid unncecssary lookups
            return ()

        tag_ids = self.tagged_items.values_list("tag_id", flat=True)
        if not tag_ids:
            # Avoid unncecssary lookups
            return ()

        # Identify 'other' live pages with tags in common
        tag_match_ids = (
            ArticlePage.objects.public()
            .live()
            .not_page(self)
            .filter(tagged_items__tag_id__in=tag_ids)
            .values_list("id", flat=True)
            .distinct()
        )
        if not tag_match_ids:
            # Avoid unncecssary lookups
            return ()

        # Use search() to prioritise items with the highest number of matches
        return tuple(
            ArticlePage.objects.filter(id__in=tag_match_ids).search(
                self.article_tag_names,
                fields=["article_tag_names"],
                operator="or",
            )[:3]
        )

    @cached_property
    def latest_items(self) -> Tuple["ArticlePage"]:
        """
        Return the three most recently published ArticlePages,
        excluding this object.
        """
        similarqueryset = list(self.similar_items)

        latestqueryset = list(
            ArticlePage.objects.public()
            .live()
            .not_page(self)
            .select_related("hero_image")
            .prefetch_related("hero_image__renditions")
            .order_by("-first_published_at")
        )
        filterlatestpages = [
            page for page in latestqueryset if page not in similarqueryset
        ]

        return tuple(filterlatestpages[:3])


class RecordArticlePage(TopicalPageMixin, ContentWarningMixin, BasePageWithIntro):
    template = "articles/record_article_page.html"
    parent_page_types = ["collections.ExplorerIndexPage"]
    subpage_types = []

    record = RecordField(verbose_name=_("record"), db_index=True)
    record.wagtail_reference_index_ignore = True

    date_text = models.CharField(
        verbose_name=_("date text"),
        max_length=100,
        help_text=_("Date(s) related to the record (max. character length: 100)"),
    )

    about = RichTextField(
        verbose_name=_("why this record matters"),
        features=settings.RESTRICTED_RICH_TEXT_FEATURES,
    )

    image_library_link = models.URLField(
        blank=True,
        verbose_name="Image library link",
        help_text="Link to an external image library",
    )

    print_on_demand_link = models.URLField(
        blank=True,
        verbose_name="Print on demand link",
        help_text="Link to an external print on demand service",
    )

    featured_highlight_gallery = models.ForeignKey(
        "collections.HighlightGalleryPage",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("featured highlight gallery"),
    )

    featured_article = models.ForeignKey(
        "articles.ArticlePage",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("featured article"),
    )

    promoted_links = StreamField(
        [("promoted_link", AuthorPromotedPagesBlock())],
        max_num=1,
        blank=True,
        null=True,
        use_json_field=True,
    )

    # DataLayerMixin overrides
    gtm_content_group = "Record articles"

    class Meta:
        verbose_name = _("record article")
        verbose_name_plural = _("record articles")

    content_panels = BasePageWithIntro.content_panels + [
        MultiFieldPanel(
            heading="Content Warning Options",
            classname="collapsible",
            children=[
                FieldPanel("display_content_warning"),
                FieldPanel("custom_warning_text"),
            ],
        ),
        InlinePanel(
            "gallery_images",
            heading="Image Gallery",
            label="Item",
            min_num=1,
            max_num=6,
        ),
        MultiFieldPanel(
            heading="Body",
            children=[
                FieldPanel("record"),
                FieldPanel("date_text"),
                FieldPanel("about"),
                FieldPanel("image_library_link"),
                FieldPanel("print_on_demand_link"),
            ],
        ),
        FieldPanel("featured_highlight_gallery"),
        FieldPanel("featured_article"),
        FieldPanel("promoted_links"),
    ]

    promote_panels = BasePageWithIntro.promote_panels + [
        TopicalPageMixin.get_topics_inlinepanel(),
        TopicalPageMixin.get_time_periods_inlinepanel(),
    ]

    search_fields = BasePageWithIntro.search_fields + [
        index.AutocompleteField("gallery_text"),
        index.AutocompleteField("date_text"),
        index.AutocompleteField("about"),
        index.AutocompleteField("topic_names", boost=1),
        index.AutocompleteField("time_period_names", boost=1),
    ]

    @cached_property
    def gallery_items(self):
        """
        Used to access the page's 'gallery_images' for output. Makes use of
        Django's select_related() and prefetch_related() to efficiently
        prefetch image and rendition data from the database.
        """
        return (
            self.gallery_images.all()
            .select_related("image")
            .prefetch_related("image__renditions")
        )

    @property
    def gallery_text(self) -> str:
        """
        Returns all of the relevant text defined on this page's gallery images,
        joined into one giant string to faciliate indexing.
        """
        strings = []
        for item in self.gallery_images.all():
            strings.extend([item.alt_text, item.caption])
            if item.has_transcription:
                strings.extend([item.transcription_header, item.transcription_text])
            if item.has_translation:
                strings.extend([item.translation_header, item.translation_text])
        return " ".join(strings)

    @cached_property
    def gallery_has_translations_transcriptions(self):
        """
        Returns boolean indicating whether this page has any gallery transcriptions or translations.
        """
        for item in self.gallery_items.all():
            if item.image.translation or item.image.transcription:
                return True
        return False


class PageGalleryImage(Orderable):
    page = ParentalKey(Page, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey(
        get_image_model_string(), on_delete=models.SET_NULL, null=True, related_name="+"
    )
    alt_text = models.CharField(
        verbose_name=_("alternative text"),
        max_length=100,
        help_text=mark_safe(
            'Alternative (alt) text describes images when they fail to load, and is read aloud by assistive technologies. Use a maximum of 100 characters to describe your image. <a href="https://html.spec.whatwg.org/multipage/images.html#alt" target="_blank">Check the guidance for tips on writing alt text</a>.'
        ),
    )
    caption = RichTextField(
        help_text="An optional caption, which will be displayed directly below the image. This could be used for image sources or for other useful metadata.",
        blank=True,
    )

    class Meta(Orderable.Meta):
        verbose_name = _("gallery image")
        verbose_name_plural = _("gallery images")

    panels = [
        FieldPanel("image"),
        FieldPanel("alt_text"),
        FieldPanel("caption"),
    ]

from typing import Any, Dict

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpRequest
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import Page

from etna.core.models import BasePage
from etna.core.serializers import (
    DefaultPageSerializer,
    ImageSerializer,
    RichTextSerializer,
)


class AuthorIndexPage(BasePage):
    """Author index page

    This is the parent page for all authors. It is used to
    display a list of authors, and to link to individual
    author pages from the list.
    """

    subpage_types = ["authors.PersonPage"]

    parent_page_types = ["home.HomePage"]

    api_fields = BasePage.api_fields + [
        APIField("author_pages", serializer=DefaultPageSerializer(many=True))
    ]

    @cached_property
    def author_pages(self):
        """Return a sample of child pages for rendering in teaser."""
        return PersonPage.objects.all().live().specific().exclude(author_summary="").exclude(author_summary=None).order_by("title")
    
    
class ResearcherIndexPage(BasePage):
    """Author index page

    This is the parent page for all authors. It is used to
    display a list of authors, and to link to individual
    author pages from the list.
    """

    subpage_types = ["authors.PersonPage"]

    parent_page_types = ["home.HomePage"]

    api_fields = BasePage.api_fields + [
        APIField("researcher_pages", serializer=DefaultPageSerializer(many=True))
    ]

    @cached_property
    def researcher_pages(self):
        """Return a sample of child pages for rendering in teaser."""
        return PersonPage.objects.all().live().specific().exclude(research_summary="").exclude(research_summary=None).order_by("title")


class PersonPage(BasePage):
    """Person page

    This page is to be used for an Person profile page, where
    we can put info about the Person, an image, and then use it
    to link pages to an Person.
    """

    role = models.CharField(blank=True, null=True, max_length=100)
    author_summary = RichTextField(
        blank=True, null=True, features=settings.RESTRICTED_RICH_TEXT_FEATURES
    )
    research_summary = RichTextField(
        blank=True, null=True, features=settings.RESTRICTED_RICH_TEXT_FEATURES
    )
    image = models.ForeignKey(
        get_image_model_string(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("image"),
        FieldPanel("role"),
        FieldPanel("author_summary"),
        FieldPanel("research_summary"),
    ]

    class Meta:
        verbose_name = "Person page"
        verbose_name_plural = "Person pages"
        verbose_name_public = "person"

    # DataLayerMixin overrides
    gtm_content_group = "Person page"

    parent_page_types = ["authors.AuthorIndexPage"]
    subpage_types = []

    default_api_fields = BasePage.default_api_fields + [
        APIField("role"),
        APIField("image", serializer=ImageSerializer(rendition_size="fill-512x512")),
        APIField(
            "image_small",
            serializer=ImageSerializer(rendition_size="fill-128x128", source="image"),
        ),
    ]

    api_fields = BasePage.api_fields + [
        APIField("role"),
        APIField("author_summary", serializer=RichTextSerializer()),
        APIField("research_summary", serializer=RichTextSerializer()),
        APIField(
            "authored_focused_articles",
            serializer=DefaultPageSerializer(
                required_api_fields=["teaser_image"], many=True
            ),
        ),
        APIField("image", serializer=ImageSerializer(rendition_size="fill-512x512")),
        APIField(
            "image_small",
            serializer=ImageSerializer(rendition_size="fill-128x128", source="image"),
        ),
    ]

    @cached_property
    def authored_focused_articles(self):
        from etna.articles.models import FocusedArticlePage

        return (
            FocusedArticlePage.objects.live()
            .public()
            .filter(pk__in=self.related_page_pks)
            .order_by("-first_published_at")
            .select_related("teaser_image")
        )

    @cached_property
    def related_page_pks(self):
        """
        Returns a list of ids of pages that have used the `AuthorTag` inline
        to indicate a relationship with this author. The values are ordered by
        when the page was first published ('more recently added' pages take presendence)
        """
        return tuple(
            self.author_pages.values_list("page_id", flat=True).order_by(
                "-page__first_published_at"
            )
        )

    def get_datalayer_data(self, request: HttpRequest) -> Dict[str, Any]:
        data = super().get_datalayer_data(request)
        data.update(customDimension3="Person page")
        return data


class AuthorTag(models.Model):
    """
    This model allows any page type to be associated with an author page.

    Add a ForeignKey with a fitting related_name (e.g. `focused_articles`
    for `FocusedArticlePage`) to the page's model to use this.
    """

    page = ParentalKey(Page, on_delete=models.CASCADE, related_name="author_tags")
    author = models.ForeignKey(
        PersonPage,
        verbose_name="author",
        related_name="author_pages",
        on_delete=models.CASCADE,
    )

    def clean(self):
        super().clean()
        if author := self.author:
            if author.author_summary == "":
                raise ValidationError(
                    {
                        "author": [
                            "An author summary is required for use as an author."
                        ]
                    }
                )


class AuthorPageMixin:
    """
    A mixin for pages that uses the ``AuthorTag`` model
    in order to be associated with an author.
    """

    @classmethod
    def get_authors_inlinepanel(cls, max_num=3):
        return InlinePanel(
            "author_tags",
            heading="Page author",
            help_text="Select the author of this page.",
            max_num=max_num,
        )

    @cached_property
    def authors(self):
        return tuple(
            item.author
            for item in self.author_tags.select_related("author").filter(
                author__live=True
            )
        )

    @property
    def author_names(self):
        """
        Returns the title of the authors to be used for indexing
        """
        if self.authors:
            return ", ".join([author.title for author in self.authors])

    api_fields = [
        APIField(
            "authors",
            serializer=DefaultPageSerializer(required_api_fields=["image"], many=True),
        )
    ]

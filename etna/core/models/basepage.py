from typing import Any, Dict

from django.conf import settings
from django.db import models
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.search import index

from wagtailmetadata.models import MetadataPageMixin

from etna.analytics.mixins import DataLayerMixin
from etna.core.cache_control import (
    apply_default_cache_control,
    apply_default_vary_headers,
)

__all__ = [
    "BasePage",
    "BasePageWithIntro",
]


@method_decorator(apply_default_vary_headers, name="serve")
@method_decorator(apply_default_cache_control, name="serve")
class BasePage(MetadataPageMixin, DataLayerMixin, Page):
    """
    An abstract base model that is used for all Page models within
    the project. Any common fields, Wagtail overrides or custom
    functionality can be added here.
    """

    teaser_text = models.TextField(
        verbose_name=_("teaser text"),
        help_text=_(
            "A short, enticing description of this page. This will appear in promos and under thumbnails around the site."
        ),
        max_length=160,
    )

    teaser_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Image that will appear on thumbnails and promos around the site."),
    )

    # Default help_text overrides
    Page._meta.get_field("slug").help_text = _(
        "The name of the page as it will appear at the end of the URL e.g. http://nationalarchives.org.uk/[slug]"
    )
    Page._meta.get_field("search_description").help_text = _(
        "The descriptive text displayed underneath a headline in search engine results and when shared on social media."
    )
    MetadataPageMixin._meta.get_field("search_image").help_text = _(
        "Image that will appear as a promo when this page is shared on social media."
    )

    # DataLayerMixin overrides
    gtm_content_group = "Page"

    promote_panels = MetadataPageMixin.promote_panels + [
        FieldPanel("teaser_image"),
        FieldPanel("teaser_text"),
    ]

    class Meta:
        abstract = True

    def get_datalayer_data(self, request: HttpRequest) -> Dict[str, Any]:
        """
        Return values that should be included in the Google Analytics datalayer
        when rendering this page.

        Override this method on subclasses to add data that is relevant to a
        specific page type.
        """
        data = super().get_datalayer_data(request)
        data.update(customDimension3=self._meta.verbose_name)
        return data


class BasePageWithIntro(BasePage):
    """
    An abstract base model for more long-form content pages that
    start with a required 'intro'.
    """

    intro = RichTextField(
        verbose_name=_("introductory text"),
        help_text=_(
            "1-2 sentences introducing the subject of the page, and explaining why a user should read on."
        ),
        features=settings.INLINE_RICH_TEXT_FEATURES,
        max_length=300,
    )

    class Meta:
        abstract = True

    content_panels = BasePage.content_panels + [FieldPanel("intro")]

    search_fields = BasePage.search_fields + [
        index.SearchField("intro", boost=3),
    ]

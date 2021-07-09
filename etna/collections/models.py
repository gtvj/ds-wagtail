from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images import get_image_model_string, get_image_model
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey

from ..alerts.models import AlertMixin
from ..teasers.models import TeaserImageMixin
from ..records.models import RecordPage
from ..records.widgets import RecordChooser
from .blocks import TimePeriodExplorerPageStreamBlock, TopicExplorerPageStreamBlock


class ExplorerIndexPage(AlertMixin, TeaserImageMixin, Page):
    """Collection Explorer landing page.

    This page is the starting point for a user's journey through the collection
    explorer.
    """

    sub_heading = models.CharField(max_length=200, blank=False)

    content_panels = Page.content_panels + [FieldPanel("sub_heading")]
    promote_panels = Page.promote_panels + TeaserImageMixin.promote_panels
    settings_panels = Page.settings_panels + AlertMixin.settings_panels

    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "collections.TopicExplorerPage",
        "collections.TimePeriodExplorerPage",
    ]

    @cached_property
    def topic_pages(self):
        """Fetch child topic explorer pages.

        Result should be suitable for rendering on the front end.
        """
        return (
            self.get_children()
            .type(TopicExplorerPage)
            .order_by("title")
            .live()
            .public()
            .specific()
        )

    @cached_property
    def time_period_pages(self):
        """Fetch child time period explorer pages.

        Result should be suitable for rendering on the front end.
        """
        return (
            self.get_children()
            .type(TimePeriodExplorerPage)
            .live()
            .public()
            .order_by("timeperiodexplorerpage__start_year")
            .specific()
        )


class TopicExplorerPage(AlertMixin, TeaserImageMixin, Page):
    """Topic explorer page.

    This page represents one of the many categories a user may select in the
    collection explorer.

    A category page is responsible for listing its child pages, which may be either
    another CategoryPage (to allow the user to make a more fine-grained choice) or a
    single ResultsPage (to output the results of their selection).
    """

    sub_heading = models.CharField(max_length=200, blank=False)

    body = StreamField(TopicExplorerPageStreamBlock, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("sub_heading"),
        StreamFieldPanel("body"),
    ]
    promote_panels = Page.promote_panels + TeaserImageMixin.promote_panels
    settings_panels = Page.settings_panels + AlertMixin.settings_panels

    @property
    def results_pages(self):
        """Fetch child results period pages for rendering on the front end."""
        return (
            self.get_children()
            .type(ResultsPage)
            .order_by("title")
            .live()
            .public()
            .specific()
        )

    parent_page_types = [
        "collections.ExplorerIndexPage",
        "collections.TopicExplorerPage",
    ]
    subpage_types = ["collections.TopicExplorerPage", "collections.ResultsPage"]


class TimePeriodExplorerPage(AlertMixin, TeaserImageMixin, Page):
    """Time period page.

    This page represents one of the many categories a user may select in the
    collection explorer.

    A category page is responsible for listing its child pages, which may be either
    another CategoryPage (to allow the user to make a more fine-grained choice) or a
    single ResultsPage (to output the results of their selection).
    """

    sub_heading = models.CharField(max_length=200, blank=False)
    body = StreamField(TimePeriodExplorerPageStreamBlock, blank=True)
    start_year = models.IntegerField(blank=False)
    end_year = models.IntegerField(blank=False)

    content_panels = Page.content_panels + [
        FieldPanel("sub_heading"),
        StreamFieldPanel("body"),
        FieldPanel("start_year"),
        FieldPanel("end_year"),
    ]
    promote_panels = Page.promote_panels + TeaserImageMixin.promote_panels
    settings_panels = Page.settings_panels + AlertMixin.settings_panels

    @property
    def results_pages(self):
        """Fetch child results period pages for rendering on the front end."""
        return (
            self.get_children()
            .type(ResultsPage)
            .order_by("title")
            .live()
            .public()
            .specific()
        )

    parent_page_types = [
        "collections.ExplorerIndexPage",
        "collections.TimePeriodExplorerPage",
    ]
    subpage_types = ["collections.TimePeriodExplorerPage", "collections.ResultsPage"]


class ResultsPage(AlertMixin, TeaserImageMixin, Page):
    """Results page.

    This page is a placeholder for the results page at the end of a user's
    journey through the collection explorer.

    Eventually this page will run an editor-defined query against the
    collections API and display the results.
    """

    sub_heading = models.CharField(max_length=200, blank=False)
    introduction = models.TextField(blank=False)

    content_panels = Page.content_panels + [
        FieldPanel("sub_heading"),
        FieldPanel("introduction"),
        InlinePanel("records", heading="Records"),
    ]
    promote_panels = Page.promote_panels + TeaserImageMixin.promote_panels
    settings_panels = Page.settings_panels + AlertMixin.settings_panels

    def get_context(self, request):
        """Fetch RecordPage instances from Kong and add to context."""
        context = super().get_context(request)

        context["results"] = []
        record_with_image = self.records.values_list("record_iaid", "teaser_image")
        for record_iaid, image_id in record_with_image:
            try:
                context["results"].append(
                    (
                        RecordPage.search.get(iaid=record_iaid),
                        get_image_model().objects.get(pk=image_id),
                    )
                )
            except ObjectDoesNotExist:
                continue

        return context

    max_count_per_parent = 1
    parent_page_types = []
    subpage_types = []


class ResultsPageRecordPage(Orderable, models.Model):
    """Map orderable records data to ResultsPage"""

    page = ParentalKey("ResultsPage", on_delete=models.CASCADE, related_name="records")
    record_iaid = models.TextField(verbose_name="Record")
    teaser_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("record_iaid", widget=RecordChooser),
        ImageChooserPanel("teaser_image"),
    ]

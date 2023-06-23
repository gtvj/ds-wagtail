import logging
import uuid

from http import HTTPStatus
from typing import Any, Dict

from django.contrib.contenttypes.models import ContentType
from django.forms import Form
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView

from wagtail.admin.auth import permission_denied
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.views.reports import ReportView
from wagtail.admin.widgets import AdminDateInput
from wagtail.models import Revision

import django_filters

from etna.feedback.constants import SentimentChoices
from etna.feedback.forms import FeedbackCommentForm, FeedbackForm
from etna.feedback.models import FeedbackPrompt, FeedbackSubmission
from etna.feedback.utils import sign_submission_id

logger = logging.getLogger(__name__)


class VersionedFeedbackViewMixin:
    """
    Mixin for view classes that are initialized from a prompt_id/version
    combination, which determine options and messaging shown to the user.
    """

    def setup(
        self,
        request: HttpRequest,
        prompt_id: uuid.UUID,
        version: int,
        **kwargs,
    ) -> None:
        super().setup(request, **kwargs)
        self.prompt_id = prompt_id
        self.version = version
        self.is_ajax = request.POST.get("is_ajax", "false") == "true"
        self.prompt_revision = get_object_or_404(
            Revision,
            content_type=ContentType.objects.get_for_model(FeedbackPrompt),
            id=version,
        )
        self.prompt = self.prompt_revision.as_object()
        if self.prompt.public_id != prompt_id:
            raise Http404("Bad prompt_id / version combination.")


@method_decorator(csrf_exempt, name="dispatch")
class FeedbackSubmitView(VersionedFeedbackViewMixin, FormView):
    """
    A view for vaidating and storing feedback submitted from a prompt.

    Since the prompt takes care of form rendering, this view only responds
    to POST requests.

    The URL includes `prompt_id` and `version` parameters, which are used to
    to determine the exact version of the prompt seen by the user, and the
    response options that were available to them.
    """

    form_class = FeedbackForm
    http_method_names = ["post"]

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update(
            response_options=self.prompt.response_options,
            response_label=self.prompt.text,
        )
        return kwargs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(prompt=self.prompt, **kwargs)

    def form_valid(self, form: Form) -> HttpResponse:
        # Initialize submission
        obj = FeedbackSubmission(
            prompt=self.prompt,
            prompt_text=self.prompt.text,
            prompt_revision=self.prompt_revision,
        )

        # Set field values from form data
        for name, value in form.cleaned_data.items():
            setattr(obj, name, value)

        # Update fields from request data
        if self.request.user.is_authenticated:
            obj.user = self.request.user

        # Save submission to the DB
        obj.save()

        if self.is_ajax:
            return JsonResponse(
                {
                    "id": str(obj.public_id),
                    "signature": sign_submission_id(obj.public_id),
                    "comment_prompt_text": form.cleaned_data["comment_prompt_text"],
                }
            )

        success_url = self.get_success_url()
        querystring = urlencode(
            {"submission": obj.public_id, "next": form.cleaned_data["url"]}
        )
        return HttpResponseRedirect(success_url + "?" + querystring)

    def form_invalid(self, form: Form) -> HttpResponse:
        data = {
            "success": False,
            "form_data": dict(form.data),
            "errors": dict(form.errors),
        }
        return JsonResponse(data=data, status=HTTPStatus.BAD_REQUEST)

    def get_success_url(self) -> str:
        return reverse(
            "feedback:success",
            kwargs={"prompt_id": self.prompt_id, "version": self.version},
        )


@method_decorator(csrf_exempt, name="dispatch")
class FeedbackCommentSubmitView(FormView):
    """A view for validating and storing comments submitted to accompany feedback.

    Because the view only needs to respond to requests posted via JS,
    it only responds to POST requests, and always returns a `JsonResponse`.
    """

    form_class = FeedbackCommentForm
    http_method_names = ["post"]

    def form_valid(self, form: Form) -> HttpResponse:
        if form.cleaned_data["comment"]:
            obj = form.cleaned_data["submission"]
            obj.comment = form.cleaned_data["comment"]
            obj.save(update_fields=["comment"])
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        data = {
            "success": False,
            "form_data": dict(form.data),
            "errors": dict(form.errors),
        }
        return JsonResponse(data=data, status=HTTPStatus.BAD_REQUEST)


class FeedbackSuccessView(VersionedFeedbackViewMixin, TemplateView):
    template_name = "feedback/success.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        try:
            submission_id = str(uuid.UUID(self.request.GET["submission"]))
        except (KeyError, ValueError):
            submission_id = None
        return super().get_context_data(
            prompt=self.prompt,
            next_url=self.request.GET.get("next", "/"),
            submission_id=submission_id,
            **kwargs,
        )


class FeedbackSubmissionFilterSet(WagtailFilterSet):
    received_from = django_filters.DateFilter(
        field_name="received_at",
        lookup_expr="date__gte",
        label=_("Date received (from)"),
        widget=AdminDateInput,
    )
    received_to = django_filters.DateFilter(
        field_name="received_at",
        lookup_expr="date__lte",
        label=_("Date received (to)"),
        widget=AdminDateInput,
    )
    response_sentiment = django_filters.ChoiceFilter(
        choices=SentimentChoices.choices, label=_("Sentiment")
    )

    class Meta:
        model = FeedbackSubmission
        fields = {
            "path": ["iexact", "istartswith"],
        }


class FeedbackSubmissionReportView(ReportView):
    title = "Feedback submissions"
    header_icon = "form"
    model = FeedbackSubmission
    is_searchable = False
    filterset_class = FeedbackSubmissionFilterSet
    template_name = "feedback/reports/submission_report.html"

    list_display = [
        "received_at",
        "path",
        "prompt_text",
        "response",
        "comment_truncated",
    ]
    list_export = [
        "id",
        "public_id",
        "received_at",
        "full_url",
        "path",
        "query_params",
        "prompt_text",
        "response_label",
        "response_sentiment",
        "sentiment_label",
        "comment_prompt_text",
        "comment",
        "prompt_id",
        "prompt_revision_id",
        "page_id",
        "page_revision_id",
        "page_revision_published",
        "user_id",
        "site_id",
    ]

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["table"].base_url = self.request.path
        return context

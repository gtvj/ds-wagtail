import datetime

from django.core.paginator import Page
from django.shortcuts import Http404, render
from django.urls import reverse
from django.utils import timezone

import pytz

from ...ciim.constants import SEARCH_URL_RETAIN_DELTA, TNA_URLS
from ...ciim.exceptions import DoesNotExist
from ...ciim.paginator import APIPaginator
from ..api import records_client


def record_disambiguation_view(request, reference_number):
    """View to render a record's details page or disambiguation page if multiple records are found.

    Details pages differ from all other page types within Etna in that their
    data isn't fetched from the CMS but an external API. And unlike standrard
    Wagtail pages, this view is accessible from a fixed URL.

    Fetches by reference_number may return multiple results.

    For example ADM 223/3. This is both the catalogue reference for 1 piece and
    for the 499 item records within:

    https://discovery.nationalarchives.gov.uk/browse/r/h/C4122893
    """
    per_page = 20
    page_number = int(request.GET.get("page", 1))
    offset = (page_number - 1) * per_page

    result = records_client.search_unified(
        web_reference=reference_number, offset=offset, size=per_page
    )

    if not result:
        raise Http404

    # if the results contain a single record page, redirect to the details page.
    if len(result) == 1:
        record = result.hits[0]
        return record_detail_view(request, record.iaid)

    paginator = APIPaginator(result.total_count, per_page=per_page)
    page = Page(result, number=page_number, paginator=paginator)

    return render(
        request,
        "records/record_disambiguation_page.html",
        {
            "record_results_page": page,
            "queried_reference_number": reference_number,
        },
    )


def record_detail_view(request, iaid):
    """View for rendering a record's details page.

    Details pages differ from all other page types within Etna in that their
    data isn't fetched from the CMS but an external API. And unlike pages, this
    view is accessible from a fixed URL.
    Sets context for Back to search button.
    """
    template_name = "records/record_detail.html"
    context = {}
    try:
        # for any record
        record = records_client.fetch(iaid=iaid, expand=True)

        # check archive record
        if record.source == "ARCHON":
            template_name = "records/archive_detail.html"
            context.update(discovery_browse=TNA_URLS.get("discovery_browse"))
    except DoesNotExist:
        raise Http404

    image = None

    # TODO: Kong open beta API does not support media. Re-enable/update once media is available.
    # if page.is_digitised:
    #     image = Image.search.filter(rid=page.media_reference_id).first()

    # Back to search - default url
    back_to_search_url = reverse("search-featured")

    # Back to search button - update url when timestamp is not expired
    if back_to_search_url_timestamp := request.session.get(
        "back_to_search_url_timestamp"
    ):
        back_to_search_url_timestamp = datetime.datetime.strptime(
            back_to_search_url_timestamp, "%Y%m%d-%H%M%S"
        )
        back_to_search_url_timestamp = back_to_search_url_timestamp.astimezone(pytz.utc)
        back_to_search_url_timestamp_delta = (
            back_to_search_url_timestamp + SEARCH_URL_RETAIN_DELTA
        )
        if timezone.now() <= back_to_search_url_timestamp_delta:
            back_to_search_url = request.session.get("back_to_search_url")

    context.update(
        record=record,
        image=image,
        meta_title=record.summary_title,
        back_to_search_url=back_to_search_url,
    )

    return render(
        request,
        template_name,
        context,
    )

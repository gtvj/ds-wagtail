from django import template
from django.conf import settings

from etna.ciim.constants import TNA_URLS, LevelKeys, NonTNALevelKeys

from ..field_labels import FIELD_LABELS
from ..models import Record

register = template.Library()


# TODO: Reduce cyclomatic complexity from 14 to 12 or below
# flake8: noqa: C901
@register.simple_tag
def record_url(
    record: Record,
    is_editorial: bool = False,
    order_from_discovery: bool = False,
) -> str:
    """
    Return the URL for the provided `record`, which should always be a
    fully-transformed `etna.records.models.Record` instance.

    use_non_reference_number_url: this serves one stop switch

    level_or_archive: Use api level name or "Archive" name. This value is checked
    with a set of values in order to override reference number that show
    disambiguation page (multiple iaid share the same reference number).

    base_record: is the original record; use when record is not the original record
    and record is a subset of the original record along with level_or_archive
    in order to determine reference number override

    form_group: use with results from search queries, value determines tna, nonTna results
    """
    if not record:
        return ""

    if is_editorial and settings.FEATURE_RECORD_LINKS_GO_TO_DISCOVERY and record.iaid:
        return TNA_URLS.get("discovery_rec_default_fmt").format(iaid=record.iaid)

    if order_from_discovery:
        if record.custom_record_type == "ARCHON":
            return TNA_URLS.get("discovery_rec_archon_fmt").format(iaid=record.iaid)
        elif record.custom_record_type == "CREATORS":
            return TNA_URLS.get("discovery_rec_creators_fmt").format(iaid=record.iaid)
        else:
            return TNA_URLS.get("discovery_rec_default_fmt").format(iaid=record.iaid)

    if record:
        return record.url
    return ""
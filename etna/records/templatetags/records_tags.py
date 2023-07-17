from django import template
from django.conf import settings

from ...ciim.constants import TNA_URLS, LevelKeys, NonTNALevelKeys
from ..field_labels import FIELD_LABELS
from ..models import Record

register = template.Library()


@register.simple_tag
def record_url(
    record: Record,
    is_editorial: bool = False,
    order_from_discovery: bool = False,
    level_or_archive: str = "",
) -> str:
    """
    Return the URL for the provided `record`, which should always be a
    fully-transformed `etna.records.models.Record` instance.

    level_or_archive: Use api level name or "Archive" name. This value is checked
    with a set of values in order to override reference number that show
    disambiguation page (multiple iaid share the same reference number).
    """
    if is_editorial and settings.FEATURE_RECORD_LINKS_GO_TO_DISCOVERY and record.iaid:
        return TNA_URLS.get("discovery_rec_default_fmt").format(iaid=record.iaid)

    if order_from_discovery:
        if record.custom_record_type == "ARCHON":
            return TNA_URLS.get("discovery_rec_archon_fmt").format(iaid=record.iaid)
        elif record.custom_record_type == "CREATORS":
            return TNA_URLS.get("discovery_rec_creators_fmt").format(iaid=record.iaid)
        else:
            return TNA_URLS.get("discovery_rec_default_fmt").format(iaid=record.iaid)

    # actual level names as level codes defined differ between tna and nonTna
    reference_number_override_list = (
        "Lettercode",  # same as Department, but returned in API response
        "Department",
        "Division",
        "Sub-series",
        "Sub-sub-series",
        "Archive",  # no level specified for this value
    )
    if record:
        if level_or_archive in reference_number_override_list:
            return record.non_reference_number_url
        else:
            return record.url
    return ""


@register.simple_tag
def is_page_current_item_in_hierarchy(page: Record, hierarchy_item: Record):
    """Checks whether given page matches item from a record's hierarchy"""
    return page.iaid == hierarchy_item.iaid


@register.filter
def as_label(record_field_name: str) -> str:
    """returns human readable label for pre configured record field name, otherwise Invalid name"""
    return FIELD_LABELS.get(record_field_name, "UNRECOGNISED FIELD NAME")


@register.simple_tag
def level_name(level_code: int, is_tna: bool) -> str:
    """returns level as a human readable string"""
    if is_tna:
        return LevelKeys["LEVEL_" + str(level_code)].value
    else:
        return NonTNALevelKeys["LEVEL_" + str(level_code)].value


@register.simple_tag
def breadcrumb_items(hierarchy: list, is_tna: bool, current_record: Record) -> list:
    """Returns breadcrumb items depending on position in hierarchy
    Update tna_breadcrumb_levels or oa_breadcrumb_levels to change the levels displayed
    """
    items = []
    tna_breadcrumb_levels = [1, 2, 3]
    oa_breadcrumb_levels = [1, 2, 5]
    for hierarchy_record in hierarchy:
        if hierarchy_record.level_code != current_record.level_code:
            if is_tna:
                if hierarchy_record.level_code in tna_breadcrumb_levels:
                    items.append(hierarchy_record)
            else:
                if hierarchy_record.level_code in oa_breadcrumb_levels:
                    items.append(hierarchy_record)
    items.append(current_record)
    if len(items) > 3:
        items = items[-3:]
    return items

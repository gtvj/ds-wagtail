from django import template
from django.conf import settings

from ...ciim.constants import TNA_URLS, LevelKeys, NonTNALevelKeys
from ..field_labels import FIELD_LABELS
from ..models import Record

register = template.Library()


@register.simple_tag
def record_url(
    record: Record, is_editorial: bool = False, order_from_discovery: bool = False
) -> str:
    """
    Return the URL for the provided `record`, which should always be a
    fully-transformed `etna.records.models.Record` instance.

    Handling of Iaid as priority to allow Iaid in disambiguation pages when
    returning more than one record
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

    return record.url if record is not None else ""


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
def breadcrumb_items(hierarchy: list, is_tna: bool, current_item: Record) -> list:
    """Returns breadcrumb items depending on position in hierarchy
    Update tna_breadcrumb_levels or oa_breadcrumb_levels to change the levels displayed
    """
    items = []
    tna_breadcrumb_levels = [1, 2, 3]
    oa_breadcrumb_levels = [1, 2, 5]
    for record in hierarchy:
        if record.level_code != current_item.level_code:
            if is_tna:
                if record.level_code in tna_breadcrumb_levels:
                    items.append(record)
            else:
                if record.level_code in oa_breadcrumb_levels:
                    items.append(record)
    items.append(current_item)
    if len(items) > 3:
        items = items[-3:]
    return items

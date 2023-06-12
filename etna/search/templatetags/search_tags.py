import datetime
import logging

from typing import Union

from django import template
from django.utils.crypto import get_random_string
from django.utils.html import escape
from django.utils.safestring import mark_safe

from ...ciim.constants import SearchTabs

register = template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag(takes_context=True)
def query_string_include(context, key: str, value: Union[str, int]) -> str:
    """Add key, value to current query string."""

    request = context["request"]

    query_dict = request.GET.copy()
    query_dict[key] = value

    return query_dict.urlencode()


@register.simple_tag(takes_context=True)
def query_string_exclude(
    context, key: str, value: Union[str, int, datetime.date]
) -> str:
    """Remove matching entry from current query string."""

    request = context["request"]

    query_dict = request.GET.copy()

    if key in (
        "opening_start_date",
        "opening_end_date",
        "created_start_date",
        "created_end_date",
    ):
        # prepare query_dict date for comparison
        # substitute unkeyed input date field value with derived value
        day = str(query_dict.getlist(f"{key}_0", "")[0]) or value.day
        month = str(query_dict.getlist(f"{key}_1", "")[0]) or value.month
        year = str(query_dict.getlist(f"{key}_2", "")[0])
        qd_dt = datetime.datetime.strptime(
            f"{day} {month} {year.zfill(4)}", "%d %m %Y"
        ).date()
        if qd_dt == value:
            query_dict.pop(f"{key}_0")
            query_dict.pop(f"{key}_1")
            query_dict.pop(f"{key}_2")
    else:
        items = query_dict.getlist(key, [])
        query_dict.setlist(key, [i for i in items if i != str(value)])

    return query_dict.urlencode()


@register.simple_tag
def render_form_fields_as_hidden(form, exclude="", exclude_on_error="") -> str:
    """
    Returns automatically generated html hidden fields for the input form.
    The hidden fields are derived from the input form less the field names from exclude/exclude_on_error.
    A random suffix is applied to html id allowing the same form to be rendered
    multiple times without field ID clashes.
    form: fields of the form to be rendered as hidden
    exclude: string of fields to be excluded if found in the form. Ex field1 field2
    exclude_on_error: String of fields which overides exclude on form error. Ex field1 field2.
    """
    html = ""

    if not exclude:
        return html

    if form.errors and exclude_on_error:
        exclude = exclude_on_error

    exclude_list = exclude.split()

    for field in form.fields:
        if field not in exclude_list:
            try:
                if value := form.cleaned_data.get(field):
                    if isinstance(value, (str, int)):
                        if field in ("q", "filter_keyword"):
                            value = escape(value)
                        html += f""" <input type="hidden" name="{field}" value="{value}" id="id_{field}_{get_random_string(3)}"> """
                    elif isinstance(value, list):
                        for value_in_list in value:
                            html += f""" <input type="hidden" name="{field}" value="{value_in_list}" id="id_{field}_{get_random_string(3)}"> """
                    elif isinstance(value, datetime.date):
                        html += f""" <input type="hidden" name="{field}_0" value="{value.day}" id="id_{field}_0_{get_random_string(3)}"> """
                        html += f""" <input type="hidden" name="{field}_1" value="{value.month}" id="id_{field}_1_{get_random_string(3)}"> """
                        html += f""" <input type="hidden" name="{field}_2" value="{value.year}" id="id_{field}_2_{get_random_string(3)}"> """
                    else:
                        logger.debug(
                            f"Type {type(value)} of the field-{field}'s value not supported in render_form_fields_as_hidden ."
                        )
            except KeyError:
                # for invalid input - example invalid date, value is not cleaned
                pass
    return mark_safe(html)


@register.filter
def search_title(search_tab) -> str:
    """
    Returns title for search tab
    """
    if search_tab == SearchTabs.ALL.value:
        label = "All search results"
    elif search_tab == SearchTabs.CATALOGUE.value:
        label = "Catalogue search results"
    elif search_tab == SearchTabs.WEBSITE.value:
        label = "Website search results"
    return label


@register.simple_tag
def extended_in_operator(lhs_operand, *rhs_operand_list) -> bool:
    """
    Input params are template tags
    Returns True when rhs_operand_list contains lhs_operand value, False otherwise
    """
    return (lhs_operand in rhs_operand_list) or False


@register.filter
def non_field_error_by_code(non_field_error_code, form) -> str:
    """
    Returns customised non field error html for the error code.
    """
    for item in form.non_field_errors().data:
        if item.code == non_field_error_code:
            error_text = item.error_list[0].message
            html = '<ul class="errorlist nonfield"><li>{error_text}</li></ul>'.format(
                error_text=error_text
            )
            return mark_safe(html)

    return ""

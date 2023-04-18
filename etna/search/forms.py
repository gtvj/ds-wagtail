from typing import Dict, List, Optional, Union

from django import forms
from django.utils.functional import cached_property

from etna.core.fields import END_OF_MONTH, DateInputField

from ..ciim.client import SortBy, SortOrder
from ..ciim.constants import (
    CATALOGUE_BUCKETS,
    COLLECTION_CHOICES,
    CUSTOM_ERROR_MESSAGES,
    LEVEL_CHOICES,
    TYPE_CHOICES,
    WEBSITE_BUCKETS,
)


class SearchFilterCheckboxList(forms.widgets.CheckboxSelectMultiple):
    template_name = "search/widgets/search-filter-checkbox-list.html"


class DynamicMultipleChoiceField(forms.MultipleChoiceField):
    """MultipleChoiceField whose choices can be updated to reflect API response data."""

    widget = SearchFilterCheckboxList

    def __init__(self, *args, **kwargs):
        self.validate_input = bool(kwargs.get("choices")) and kwargs.pop(
            "validate_input", True
        )
        super().__init__(*args, **kwargs)
        # The following attribue is used in templates to prevent rendering
        # unless choices have been updated to reflect options from the API
        self.choices_updated = False
        self.configured_choices = self.choices

    def valid_value(self, value):
        """Disable validation if the field choices are not yet set."""
        if not self.validate_input:
            return True
        return super().valid_value(value)

    @cached_property
    def configured_choice_labels(self):
        return {value: label for value, label in self.configured_choices}

    def choice_label_from_api_data(self, data: Dict[str, Union[str, int]]) -> str:
        count = f"{data['doc_count']:,}"
        try:
            # Use a label from the configured choice values, if available
            return f"{self.configured_choice_labels[data['key']]} ({count})"
        except KeyError:
            # Fall back to using the key value (which is the same in most cases)
            return f"{data['key']} ({count})"

    def update_choices(
        self,
        choice_data: List[Dict[str, Union[str, int]]],
        selected_values: Optional[List[Union[str, int]]] = (),
    ):
        """
        Updates this fields `choices` list using aggregation data from the most recent
        API result. If `selected_values` is provided, options with values matching items
        in that list will be preserved in the new `choices` list, even if they are not
        present in `choice_data`.

        Expected `choice_data` format:
        [
            {
                "key": "item",
                "doc_count": 10
            },
            …
        ]
        """

        # Generate a new list of choices
        choice_vals_with_hits = set()
        choices = []
        for item in choice_data:
            choices.append((item["key"], self.choice_label_from_api_data(item)))
            choice_vals_with_hits.add(item["key"])

        for missing_value in [
            v for v in selected_values if v not in choice_vals_with_hits
        ]:
            try:
                label_base = self.configured_choice_labels[missing_value]
            except KeyError:
                label_base = missing_value
            choices.append((missing_value, f"{label_base} (0)"))

        # Order alphabetically
        choices.sort(key=lambda x: x[1])

        # Replace the field's attribute value
        self.choices = choices

        # Indicate that this field is okay to be rendered
        self.choices_updated = True


class FeaturedSearchForm(forms.Form):
    q = forms.CharField(
        label="Search here",
        # If no query is provided, pass None to client to fetch all results.
        empty_value=None,
        required=False,
        widget=forms.TextInput(attrs={"class": "search-results-hero__form-search-box"}),
    )


class BaseCollectionSearchForm(forms.Form):
    """
    NOTE: For dynamic fields (where choices are update from the API result), the field
    name should be a lower-case/underscored version of the API filter name (which are
    typically in in 'camelCase'). For example:

    "fieldname" -> "fieldname"
    "fieldName" -> "field_name"
    """

    q = forms.CharField(
        label="Search term",
        # If no query is provided, pass None to client to fetch all results.
        empty_value=None,
        required=False,
        widget=forms.TextInput(attrs={"class": "search-results-hero__form-search-box"}),
    )
    filter_keyword = forms.CharField(
        label="Search within",
        # If no filter_keyword is provided, pass None to client bypass search within
        empty_value=None,
        required=False,
        widget=forms.TextInput(attrs={"class": "search-filters__search"}),
    )
    # Choices are supplied to this field to benefit validation. The labels
    # are the same as the API supplied values, so aren't of much benefit
    level = DynamicMultipleChoiceField(
        label="Level",
        choices=LEVEL_CHOICES,
        required=False,
    )
    topic = DynamicMultipleChoiceField(
        label="Topics",
        required=False,
    )
    # Choices are supplied to this field to influence labels only. The options
    # are not complete enough to be used for validation
    collection = DynamicMultipleChoiceField(
        label="Collections",
        choices=COLLECTION_CHOICES,
        required=False,
        validate_input=False,
    )
    closure = DynamicMultipleChoiceField(
        label="Closure Status",
        required=False,
    )
    catalogue_source = DynamicMultipleChoiceField(
        label="Catalogue Sources",
        required=False,
    )
    held_by = DynamicMultipleChoiceField(
        label="Held By",
        required=False,
    )
    # Choices are supplied to this field to influence labels only. The options
    # are not complete enough to be used for validation
    type = DynamicMultipleChoiceField(
        label="Creator type",
        choices=TYPE_CHOICES,
        required=False,
        validate_input=False,
    )
    opening_start_date = DateInputField(
        label="From",
        required=False,
        default_day=1,
        default_month=1,
    )
    opening_end_date = DateInputField(
        label="To",
        required=False,
        default_day=END_OF_MONTH,
        default_month=12,
    )
    per_page = forms.IntegerField(
        min_value=20,
        max_value=50,
        required=False,
    )
    sort_by = forms.ChoiceField(
        label="Sort by",
        choices=[
            (SortBy.RELEVANCE.value, "Relevance"),
            (SortBy.DATE_OPENING.value, "Date"),
            (SortBy.TITLE.value, "Title"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "search-sort-view__form-select"}),
    )
    sort_order = forms.ChoiceField(
        label="Sort order",
        choices=[
            (SortOrder.ASC.value, "Ascending"),
            (SortOrder.DESC.value, "Descending"),
        ],
        required=False,
    )
    display = forms.ChoiceField(
        choices=[
            ("grid", "Grid"),
            ("list", "List"),
        ],
        required=False,
    )

    def clean(self):
        """Collect selected filters to pass to the client in view."""
        cleaned_data = super().clean()

        try:
            if cleaned_data.get("opening_start_date") > cleaned_data.get(
                "opening_end_date"
            ):
                self.add_error(
                    "opening_start_date",
                    CUSTOM_ERROR_MESSAGES.get("invalid_date_range"),
                )
        except TypeError:
            # Either one or both date fields are empty. No further validation necessary.
            pass

        return cleaned_data


class CatalogueSearchForm(BaseCollectionSearchForm):
    group = forms.ChoiceField(
        label="bucket",
        choices=CATALOGUE_BUCKETS.as_choices(),
        required=False,
    )


class WebsiteSearchForm(BaseCollectionSearchForm):
    group = forms.ChoiceField(
        label="bucket",
        choices=WEBSITE_BUCKETS.as_choices(),
        required=False,
    )

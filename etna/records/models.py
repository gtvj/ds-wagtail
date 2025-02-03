from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, Union

from django.conf import settings
from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from pyquery import PyQuery as pq

from etna.analytics.mixins import DataLayerMixin
from etna.ciim.constants import (
    ARCHIVE_NRA_RECORDS_COLLECTION,
    ARCHIVE_RECORD_CREATORS_COLLECTION,
    TNA_URLS,
)
from etna.ciim.models import APIModel
from etna.ciim.utils import (
    NOT_PROVIDED,
    ValueExtractionError,
    extract,
    find,
    find_all,
    format_link,
    strip_html,
)
from etna.records.classes import (
    AccessionsInfo,
    ArchiveCollections,
    CollectionInfo,
    ContactInfo,
    FurtherInfo,
)

from .converters import IAIDConverter

logger = logging.getLogger(__name__)


class Record(DataLayerMixin, APIModel):
    """A 'lazy' data-interaction layer for record data retrieved from the Client API"""

    def __init__(self, raw_data: Dict[str, Any]):
        """
        This method recieves the raw JSON data dict recieved from
        Client API and makes it available to the instance as `self._raw`.
        """
        self._raw = raw_data.get("_source") or raw_data
        self.score = raw_data.get("_score")
        self.highlights = raw_data.get("highlight") or {}

    @classmethod
    def from_api_response(cls, response: dict) -> Record:
        return cls(response)

    def __str__(self):
        return f"{self.summary_title} ({self.iaid})"

    def get(self, key: str, default: Optional[Any] = NOT_PROVIDED):
        """
        Attempts to extract `key` from `self._raw` and return the value.

        Raises `ciim.utils.ValueExtractionError` if the value cannot be extracted.
        """
        if "." in key:
            return extract(self._raw, key, default)
        try:
            return self._raw[key]
        except KeyError as e:
            if default is NOT_PROVIDED:
                raise ValueExtractionError(str(e))
            return default

    @cached_property
    def template(self) -> Dict[str, Any]:
        return self.get("@template.details", default=self.get("@template.results", {}))

    @cached_property
    def iaid(self) -> str:
        """
        Return the "iaid" value for this record. If the data is unavailable,
        or is not a valid iaid, a blank string is returned.
        """
        try:
            candidate = self.template["iaid"]
        except KeyError:
            candidate = self.get("@admin.id", default="")

        try:
            # fallback for Record Creators
            if not candidate:
                candidate = self.template["primaryIdentifier"]
        except KeyError:
            candidate = ""

        if candidate and re.match(IAIDConverter.regex, candidate):
            # value is not guaranteed to be a valid 'iaid', so we must
            # check it before returning it as one
            return candidate
        return ""

    @cached_property
    def reference_number(self) -> str:
        """
        Return the "reference_number" value for this record, or a blank
        string if no such value can be found in the usual places.
        """
        try:
            return self.template["referenceNumber"]
        except KeyError:
            pass
        identifiers = self.get("identifier", ())
        for item in identifiers:
            try:
                return item["reference_number"]
            except KeyError:
                pass
        return ""

    def reference_prefixed_summary_title(self):
        return f"{self.reference_number or 'N/A'} - {self.summary_title}"

    @cached_property
    def source_url(self):
        """
        Return the "url" value for this record. This value is typically
        only present for 'interpretive' results from other websites.

        Raises `ValueExtractionError` when the raw data does not include
        values in any of the expected positions.
        """
        try:
            return self.template["sourceUrl"]
        except KeyError:
            raise ValueExtractionError(
                f"'source_url' could not be extracted from source data: {self._raw}"
            )

    def has_source_url(self) -> bool:
        """
        Returns `True` if a 'source_url' value can be extracted from the raw data
        for this record. Otherwise `False`.
        """
        try:
            self.source_url
        except ValueExtractionError:
            return False
        else:
            return True

    @cached_property
    def summary_title(self) -> str:
        if raw := self._get_raw_summary_title():
            return mark_safe(strip_html(raw, preserve_marks=True, ensure_spaces=True))
        return raw

    def _get_raw_summary_title(self) -> str:
        try:
            return "... ".join(self.highlights["@template.details.summaryTitle"])
        except KeyError:
            pass
        try:
            return self.template["summaryTitle"]
        except KeyError:
            pass
        return self.get("summary.title", default="")

    def get_url(self, use_reference_number: bool = True) -> str:
        if use_reference_number and self.reference_number:
            try:
                return reverse(
                    "details-page-human-readable",
                    kwargs={"reference_number": self.reference_number},
                )
            except NoReverseMatch:
                pass
        if self.iaid:
            try:
                return reverse(
                    "details-page-machine-readable", kwargs={"iaid": self.iaid}
                )
            except NoReverseMatch:
                pass

        if self.has_source_url():
            return self.source_url
        return ""

    @cached_property
    def url(self) -> str:
        return self.get_url()
    
    @cached_property
    def non_reference_number_url(self) -> str:
        return self.get_url(use_reference_number=False)

    @cached_property
    def source(self) -> str:
        return self.get("source.value", default="")

    @cached_property
    def parent(self) -> Union["Record", None]:
        if parent_data := self.get("parent.0", default=None):
            return Record(parent_data)

    @cached_property
    def title(self) -> str:
        return mark_safe(self.template.get("title", ""))
    
import json
import unittest

from copy import deepcopy

from django.conf import settings
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

import responses

from ...ciim.tests.factories import create_media, create_record, create_response
from ...ciim.utils import ValueExtractionError
from ..api import get_records_client
from ..models import Image, Record


class RecordModelTests(SimpleTestCase):
    fixture_path = f"{settings.BASE_DIR}/etna/ciim/tests/fixtures/record.json"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.records_client = get_records_client()
        with open(cls.fixture_path, "r") as f:
            cls.fixture_contents = json.loads(f.read())

    def setUp(self):
        self.record = Record(deepcopy(self.fixture_contents["hits"]["hits"][0]))

    def test_template_uses_detail_template_when_present(self):
        self.assertIn("details", self.record._raw["@template"])
        self.assertEqual(self.record.template, self.record._raw["@template"]["details"])

    def test_template_uses_results_template_if_details_template_not_present(self):
        self.assertIn("results", self.record._raw["@template"])

        # patch raw data
        self.record._raw["@template"].pop("details")

        self.assertEqual(self.record.template, self.record._raw["@template"]["results"])

    def test_template_returns_empty_dict_when_no_template_available(self):
        # patch raw data
        self.record._raw["@template"] = {}
        self.assertEqual(self.record.template, {})

    def test_iaid(self):
        self.assertEqual(self.record.iaid, "C10297")

    def test_returns_blank_string_when_data_not_present(self):
        # patch raw data
        self.record._raw["@admin"].pop("id")
        self.record._raw["@template"]["details"].pop("iaid")
        self.assertEqual(self.record.iaid, "")

    def test_returns_blank_string_when_iaid_value_is_invalid(self):
        # patch raw data
        invalid_value = "bp-299"
        self.record._raw["@admin"]["id"] = invalid_value
        self.record._raw["@template"]["details"]["iaid"] = invalid_value
        self.assertEqual(self.record.iaid, "")

    def test_summary_title(self):
        self.assertEqual(
            self.record.summary_title,
            "Law Officers' Department: Registered Files",
        )

    def test_reference_number(self):
        self.assertEqual(self.record.reference_number, "LO 2")

    def test_raises_valueextractionerror_when_reference_number_is_not_present(self):
        # patch raw data
        self.record._raw.pop("identifier")
        self.record._raw["@template"]["details"].pop("referenceNumber")

        self.assertEqual(self.record.reference_number, "")

    def test_source_url(self):
        # patch raw data
        url = "http://dummy.com"
        self.record._raw["@template"]["details"]["sourceUrl"] = url

        self.assertTrue(self.record.has_source_url())
        self.assertEqual(self.record.source_url, url)

    def test_raises_valueextractionerror_if_url_not_present(self):
        self.assertFalse(self.record.has_source_url())
        with self.assertRaises(ValueExtractionError):
            self.record.source_url

    def test_url_prefers_iaid_over_reference_number_and_source_url(self):
        record = Record(
            {
                "@template": {
                    "details": {
                        "iaid": "e7e92a0b-3666-4fd6-9dac-9d9530b0888c",
                        "referenceNumber": "2515/300/1",
                        "sourceUrl": "https://www.example.com",
                    }
                }
            }
        )
        self.assertEqual(
            record.url,
            reverse("details-page-machine-readable", kwargs={"iaid": record.iaid}),
        )

    def test_url_prefers_reference_number_over_source_url(self):
        record = Record(
            {
                "@template": {
                    "details": {
                        "referenceNumber": "2515/300/1",
                        "sourceUrl": "https://www.example.com",
                    }
                }
            }
        )
        self.assertEqual(
            record.url,
            reverse(
                "details-page-human-readable",
                kwargs={"reference_number": record.reference_number},
            ),
        )

    def test_url_uses_source_url_when_no_iaid_or_reference_number_is_available(self):
        record = Record(
            {
                "@template": {
                    "details": {
                        "sourceUrl": "https://www.example.com",
                    }
                }
            }
        )
        self.assertEqual(record.url, record.source_url)

    def test_url_returns_blank_string_when_no_sutiable_data_is_present(self):
        record = Record(
            {
                "@template": {
                    "details": {
                        "summaryTitle": "A very incomplete record",
                    }
                }
            }
        )
        self.assertEqual(record.url, "")

    def test_description(self):
        self.assertEqual(
            self.record.description,
            (
                "\nThis series contains papers concering a wide variety of legal matters referred "
                "to the Law Officers for their advice or approval and includes applications for the "
                "Attorney General's General Fiat for leave to appeal to the House of Lords in criminal "
                "cases."
                "\nAlso included are a number of opinions, more of which can be found in LO 3"
            ),
        )

    def test_date_created(self):
        self.assertEqual(self.record.date_created, "1885-1979")

    def test_legal_status(self):
        self.assertEqual(self.record.legal_status, "Public Record(s)")

    def test_held_by(self):
        self.assertEqual(self.record.held_by, "The National Archives, Kew")

    def test_parent(self):
        r = self.record.parent
        self.assertEqual(
            (r.iaid, r.reference_number, r.summary_title),
            (
                "C199",
                "LO",
                "Records created or inherited by the Law Officers' Department",
            ),
        )

    def test_hierarchy(self):
        self.assertEqual(
            [
                (r.level_code, r.reference_number, r.summary_title)
                for r in self.record.hierarchy
            ],
            [
                (
                    None,
                    "LO",
                    "Records created or inherited by the Law Officers' Department",
                ),
                (
                    None,
                    "LO 2",
                    "Law Officers' Department: Registered Files",
                ),
                (
                    None,
                    "ADM 171",
                    "Admiralty, and Ministry of Defence, Navy Department: Medal Rolls",
                ),
            ],
        )

    def test_is_digitised_returns_false_when_data_not_present(self):
        self.assertEqual(self.record.is_digitised, False)

    def test_is_digitised_returns_true_when_true_value_present(self):
        # patch raw data
        self.record._raw["digitised"] = True
        self.assertEqual(self.record.is_digitised, True)

    def test_is_digitised_returns_false_when_false_value_present(self):
        # patch raw data
        self.record._raw["digitised"] = False
        self.assertEqual(self.record.is_digitised, False)

    @unittest.skip("Data not supported for the json record")
    def test_delivery_option(self):
        self.assertEqual(self.record.delivery_option, "DigitizedDiscovery")

    @unittest.skip("Data not supported for the json record")
    def test_availability_delivery_surrogates(self):
        self.assertEqual(
            self.record.availability_delivery_surrogates,
            [
                {
                    "type": "surrogate",
                    "value": (
                        '<a target="_blank" href="http://www.thegenealogist.co.uk/non-conformist-records">'
                        "The Genealogist"
                        "</a>"
                    ),
                },
                {
                    "type": "surrogate",
                    "value": (
                        '<a target="_blank" href="http://search.ancestry.co.uk/search/db.aspx?dbid=5111">'
                        "Ancestry"
                        "</a>"
                    ),
                },
            ],
        )

    def test_is_tna_default(self):
        # The test fixture includes the following, so this should
        # return True by default
        self.assertIs(self.record.is_tna, True)

    def test_is_tna_returns_false_if_group_is_non_tna(self):
        # patch raw data
        for group in self.record._raw["@datatype"]["group"]:
            if group["value"] == "tna":
                group["value"] = "nonTna"
        self.assertIs(self.record.is_tna, False)

    def test_is_tna_returns_false_if_datatype_not_present(self):
        # patch raw data
        self.record._raw.pop("@datatype")
        self.assertIs(self.record.is_tna, False)

    @unittest.skip("Data not supported for the json record")
    def test_topics(self):
        self.assertEqual(
            self.record.topics,
            [
                {
                    "title": "Taxonomy One",
                },
                {
                    "title": "Taxonomy Two",
                },
                {
                    "title": "Taxonomy Three",
                },
            ],
        )

    def test_next_record(self):
        r = self.record.next_record
        self.assertEqual(
            (r.iaid, r.reference_number, r.summary_title),
            ("C10298", "LO 1", "Law Officers' Department: Law Officers' Opinions"),
        )

    def test_previous_record(self):
        r = self.record.previous_record
        self.assertEqual(
            (r.iaid, r.reference_number, r.summary_title),
            ("C10296", "LO 3", "Law Officers' Department: Patents for Inventions"),
        )

    @unittest.skip("Data not supported for the json record")
    def test_related_records(self):
        self.assertEqual(
            [(r.iaid, r.summary_title) for r in self.record.related_records],
            [
                (
                    "C8981250",
                    "[1580-1688]. Notes (cards) from State Papers Foreign, Royal "
                    "Letters, SP 102/61. Manuscript.",
                )
            ],
        )

    @unittest.skip("Data not supported for the json record")
    def test_related_articles(self):
        self.assertEqual(
            [(r.summary_title, r.url) for r in self.record.related_articles],
            [
                (
                    "Irish maps c.1558-c.1610",
                    (
                        "http://www.nationalarchives.gov.uk/help-with-your-research/research-guides/"
                        "irish-maps-c1558-c1610/"
                    ),
                )
            ],
        )

    def test_catalogue_source(self):
        self.assertEqual(self.record.catalogue_source, "CAT")

    def test_repo_summary_title(self):
        self.assertEqual(self.record.repo_summary_title, "The National Archives")

    def test_repo_archon_value(self):
        self.assertEqual(self.record.repo_archon_value, "66")

    def test_level_code(self):
        self.assertEqual(self.record.level_code, 3)

    def test_level(self):
        self.assertEqual(self.record.level, "Series")

    def test_related_materials(self):
        self.assertEqual(
            self.record.related_materials,
            (
                {
                    "description": "For files of the tri-service Defence Intelligence staff see,",
                    "links": [
                        {
                            "id": "C5789",
                            "text": "DEFE 31",
                            "href": "/catalogue/id/C5789/",
                        }
                    ],
                },
                {
                    "description": "For records of the Joint Intelligence Bureau see",
                    "links": [
                        {
                            "id": "C14457",
                            "text": "WO 252",
                            "href": "/catalogue/id/C14457/",
                        }
                    ],
                },
                {
                    "description": "Records of the Government Code and Cypher School:",
                    "links": [],
                },
            ),
        )


@override_settings(KONG_CLIENT_BASE_URL="https://kong.test")
class UnexpectedParsingIssueTest(SimpleTestCase):
    """A collection of tests verifying fixes for real-world (but unexpected)
    issues with data returned by Kong"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.records_client = get_records_client()

    @responses.activate
    def test_hierarchy_with_no_identifier_is_skipped(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(
                        iaid="C123456",
                        hierarchy=[
                            {
                                "@summary": {
                                    "title": (
                                        "Foreign and Commonwealth Office and predecessors: "
                                        "Cultural Relations Departments:..."
                                    )
                                },
                            },
                        ],
                    ),
                ]
            ),
        )

        record = self.records_client.fetch(iaid="C123456")

        self.assertEqual(record.hierarchy, ())

    @responses.activate
    def test_record_with_origination_but_no_date(self):
        record = create_record(
            iaid="C123456",
        )
        del record["_source"]["origination"]["date"]

        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(records=[record]),
        )

        record = self.records_client.fetch(iaid="C123456")

        self.assertEqual(record.date_created, "")

    @responses.activate
    def test_related_record_with_no_identifier(self):
        record = create_record(
            related=[
                {
                    "@admin": {
                        "id": "C568",
                        "uuid": "216d37d3-eb15-3e76-99d2-bc9ee99104ce",
                    },
                    "@entity": "reference",
                    "@link": {
                        "note": {
                            "value": "For records originating in the Exchequer see"
                        },
                        "qualifier": "association",
                        "relationship": {"value": "related"},
                    },
                    "summary": {
                        "title": "Records of the Office of First Fruits and Tenths"
                    },
                }
            ],
        )

        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(records=[record]),
        )

        record = self.records_client.fetch(iaid="C123456")

        # Related records with no 'identifer' and therefore no
        # reference_nubmers were skipped but now we're linking to the details
        # page using the iaid, these records should be present
        self.assertEqual(
            [(r.iaid, r.summary_title) for r in record.related_records],
            [
                ("C568", "Records of the Office of First Fruits and Tenths"),
            ],
        )

    @responses.activate
    def test_related_article_with_no_title(self):
        record = create_record(
            iaid="C123456",
            related=[
                {
                    "@admin": {
                        "id": "rg-1582",
                        "source": "wagtail-es",
                        "uuid": "890bc89e-9c9d-37a8-bdd4-1213bad92a33",
                    },
                    "@entity": "reference",
                    "@type": {"base": "media", "type": "research guide"},
                    "source": {
                        "location": (
                            "http://www.nationalarchives.gov.uk/"
                            "help-with-your-research/research-guides/famous-wills-1552-1854/"
                        )
                    },
                }
            ],
        )

        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(records=[record]),
        )

        record = self.records_client.fetch(iaid="C123456")

        self.assertEqual(record.related_articles, ())


@unittest.skip(
    "Kong open beta API does not support media. Re-enable/update once media is available."
)
@override_settings(
    KONG_CLIENT_BASE_URL="https://kong.test",
    KONG_IMAGE_PREVIEW_BASE_URL="https://media.preview/",
)
class ImageTestCase(TestCase):
    @responses.activate
    def test_thumbnail_url(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(
                records=[
                    create_media(
                        thumbnail_location="path/to/thumbnail.jpeg",
                        location="path/to/image.jpeg",
                    ),
                ]
            ),
        )

        images = Image.search.filter(rid="")
        image = images[0]

        self.assertEquals(
            image.thumbnail_url, "https://media.preview/path/to/thumbnail.jpeg"
        )

    @responses.activate
    def test_thumbnail_url_fallback(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(
                records=[
                    create_media(
                        thumbnail_location=None, location="path/to/image.jpeg"
                    ),
                ]
            ),
        )

        images = Image.search.filter(rid="")
        image = images[0]

        # Fallback serves image through Wagtail instead of from kong
        self.assertEquals(image.thumbnail_url, "/records/image/path/to/image.jpeg")

from django.test import SimpleTestCase, override_settings

from etna.records.models import Record
from etna.records.templatetags.records_tags import (
    breadcrumb_items,
    is_page_current_item_in_hierarchy,
    level_name,
    record_url,
)


class TestRecordURLTag(SimpleTestCase):
    record_instance = Record(
        raw_data={
            "level": {
                "code": 2,
            },
            "repository": {
                "@admin": {
                    "id": "A13531109",
                },
                "identifier": [
                    {
                        "primary": True,
                        "reference_number": "66",
                        "type": "reference number",
                        "value": "66",
                    },
                    {"type": "Archon number", "value": "66"},
                ],
            },
            "@template": {
                "details": {
                    "iaid": "e7e92a0b-3666-4fd6-9dac-9d9530b0888c",
                    "referenceNumber": "2515/300/1",
                    "summaryTitle": "Test",
                }
            },
        }
    )

    tna_record_instance = Record(
        raw_data={
            "@datatype": {
                "base": "aggregation",
                "group": [{"value": "aggregation"}, {"value": "tna"}],
            },
            "@hierarchy": [
                [
                    {
                        "@admin": {
                            "id": "C4",
                            "uuid": "9d7b9dbc-0bff-304f-98f1-8bdf2de76950",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "ADM",
                                "type": "reference number",
                                "value": "ADM",
                            }
                        ],
                        "level": {"code": 1},
                        "source": {"value": "CAT"},
                        "summary": {
                            "title": "Records of the Admiralty, Naval Forces, Royal Marines, Coastguard, and related bodies"
                        },
                    },
                    {
                        "@admin": {
                            "id": "C714",
                            "uuid": "833d380a-1303-3fa1-ab16-a529d080150b",
                        },
                        "@entity": "reference",
                        "level": {"code": 2},
                        "source": {"value": "CAT"},
                        "summary": {"title": "Records of Naval Staff Departments"},
                    },
                    {
                        "@admin": {
                            "id": "C1931",
                            "uuid": "84e8175b-c6f7-3103-ad92-bfbc38e65668",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "ADM 223",
                                "type": "reference number",
                                "value": "ADM 223",
                            }
                        ],
                        "level": {"code": 3},
                        "source": {"value": "CAT"},
                        "summary": {
                            "title": "Admiralty: Naval Intelligence Division and Operational Intelligence Centre: Intelligence..."
                        },
                    },
                ]
            ],
            "level": {
                "code": 3,
            },
            "repository": {
                "@admin": {
                    "id": "A13531109",
                },
                "identifier": [
                    {
                        "primary": True,
                        "reference_number": "66",
                        "type": "reference number",
                        "value": "66",
                    },
                    {"type": "Archon number", "value": "66"},
                ],
            },
            "@template": {
                "details": {
                    "iaid": "e7e92a0b-3666-4fd6-9dac-9d9530b0888c",
                    "referenceNumber": "2515/300/1",
                    "summaryTitle": "Test",
                }
            },
        }
    )

    tna_long_hierarchy_record_instance = Record(
        raw_data={
            "@datatype": {
                "base": "aggregation",
                "group": [{"value": "aggregation"}, {"value": "tna"}],
            },
            "level": {
                "code": 7,
            },
            "repository": {
                "@admin": {
                    "id": "A13530124",
                },
            },
            "@hierarchy": [
                [
                    {
                        "@admin": {
                            "id": "C162",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "J",
                                "type": "reference number",
                                "value": "J",
                            }
                        ],
                        "level": {"code": 1},
                    },
                    {
                        "@admin": {
                            "id": "C678",
                        },
                        "@entity": "reference",
                        "level": {"code": 2},
                    },
                    {
                        "@admin": {
                            "id": "C9685",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "J 77",
                                "type": "reference number",
                                "value": "J 77",
                            }
                        ],
                        "level": {"code": 3},
                    },
                    {
                        "@admin": {
                            "id": "C81319",
                        },
                        "@entity": "reference",
                        "level": {"code": 4},
                    },
                    {
                        "@admin": {
                            "id": "C5947536",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "J 77/3417",
                                "type": "reference number",
                                "value": "J 77/3417",
                            }
                        ],
                        "level": {"code": 6},
                    },
                    {
                        "@admin": {
                            "id": "C8077549",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "J 77/3417/4284",
                                "type": "reference number",
                                "value": "J 77/3417/4284",
                            }
                        ],
                        "level": {"code": 7},
                    },
                ]
            ],
            "@template": {
                "details": {
                    "iaid": "C8077549",
                    "referenceNumber": "J 77/3417/4284",
                    "summaryTitle": "Test record",
                }
            },
        }
    )

    long_hierarchy_record_instance = Record(
        raw_data={
            "level": {
                "code": 11,
            },
            "repository": {
                "@admin": {
                    "id": "A13532972",
                },
            },
            "@hierarchy": [
                [
                    {
                        "@admin": {
                            "id": "278e5baf-af95-4b8a-a246-7bbd4faebe92",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-ADM-01 to LU-WIR-16; LU-AC-01",
                                "type": "reference number",
                                "value": "LU-ADM-01 to LU-WIR-16; LU-AC-01",
                            }
                        ],
                        "level": {"code": 1},
                    },
                    {
                        "@admin": {
                            "id": "16131aa0-f1d9-42a5-8488-e9a236366b4b",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-ADM-01 to LU-WIR-16; LU-AC-01",
                                "type": "reference number",
                                "value": "LU-ADM-01 to LU-WIR-16; LU-AC-01",
                            }
                        ],
                        "level": {"code": 2},
                    },
                    {
                        "@admin": {
                            "id": "2dba8c17-0f69-4a53-b918-e6ddb06c41a7",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-PEP-01 to LU-PEP-42; Blue Drawer 2B14 & 2B13; LU-WAR-30; LU-AC-01",
                                "type": "reference number",
                                "value": "LU-PEP-01 to LU-PEP-42; Blue Drawer 2B14 & 2B13; LU-WAR-30; LU-AC-01",
                            }
                        ],
                        "level": {"code": 5},
                    },
                    {
                        "@admin": {
                            "id": "a6f76935-7e8d-451d-ac10-b5e6a0dd0efb",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-PEP-02 to LU-PEP-42; Blue Drawer 2B14",
                                "type": "reference number",
                                "value": "LU-PEP-02 to LU-PEP-42; Blue Drawer 2B14",
                            }
                        ],
                        "level": {"code": 6},
                    },
                    {
                        "@admin": {
                            "id": "fd77b34e-db7e-4b8f-93d2-2257e66e3d96",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-PEP-27; LU-PEP-30 to LU-PEP-42",
                                "type": "reference number",
                                "value": "LU-PEP-27; LU-PEP-30 to LU-PEP-42",
                            }
                        ],
                        "level": {"code": 7},
                    },
                    {
                        "@admin": {
                            "id": "fa5e6d5f-7838-4d4c-b168-2b983b70c0b3",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-PEP-27; LU-PEP-30 to LU-PEP-42; LU-AC-01",
                                "type": "reference number",
                                "value": "LU-PEP-27; LU-PEP-30 to LU-PEP-42; LU-AC-01",
                            }
                        ],
                        "level": {"code": 8},
                    },
                    {
                        "@admin": {
                            "id": "b5da3728-3977-485a-b4bf-c1949abe5c73",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-PEP-38",
                                "type": "reference number",
                                "value": "LU-PEP-38",
                            }
                        ],
                        "level": {"code": 9},
                    },
                    {
                        "@admin": {
                            "id": "dc02e42c-043b-4d49-bade-339c851a6019",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-PEP-41",
                                "type": "reference number",
                                "value": "LU-PEP-41",
                            }
                        ],
                        "level": {"code": 10},
                    },
                    {
                        "@admin": {
                            "id": "66787951-2237-4f8a-882f-0ac275fe2bff",
                        },
                        "@entity": "reference",
                        "identifier": [
                            {
                                "primary": "true",
                                "reference_number": "LU-PEP-41",
                                "type": "reference number",
                                "value": "LU-PEP-41",
                            }
                        ],
                        "level": {"code": 11},
                    },
                ]
            ],
            "@template": {
                "details": {
                    "iaid": "66787951-2237-4f8a-882f-0ac275fe2bff",
                    "referenceNumber": "LU-PEP-41",
                    "summaryTitle": "Test record",
                }
            },
        }
    )

    record_instance_no_reference = Record(
        raw_data={
            "@template": {
                "details": {
                    "iaid": "e7e92a0b-3666-4fd6-9dac-9d9530b0888c",
                    "summaryTitle": "Test",
                }
            }
        }
    )

    interpretive_record = Record(
        raw_data={
            "@template": {
                "details": {
                    "iaid": "ip-3162",
                    "summaryTitle": "Insights page",
                    "sourceUrl": "https://www.example.com",
                }
            }
        }
    )

    records_various = [
        (
            "ARCHON",
            Record(
                raw_data={
                    "source": {"value": "ARCHON"},
                    "@template": {
                        "details": {
                            "iaid": "A123456789",
                            "referenceNumber": "154",
                        }
                    },
                }
            ),
            "https://discovery.nationalarchives.gov.uk/details/a/A123456789",
        ),
        (
            "PROCAT",
            Record(
                raw_data={
                    "source": {"value": "CAT"},
                    "@template": {
                        "details": {
                            "iaid": "C12345678",
                            "referenceNumber": "AIR 79/1711/189046",
                        }
                    },
                }
            ),
            "https://discovery.nationalarchives.gov.uk/details/r/C12345678",
        ),
        (
            "ePRO",
            Record(
                raw_data={
                    "source": {"value": "CAT"},
                    "@template": {
                        "details": {
                            "iaid": "D1234567",
                            "referenceNumber": "WO 372/2/47705",
                        }
                    },
                }
            ),
            "https://discovery.nationalarchives.gov.uk/details/r/D1234567",
        ),
        (
            "CREATORS",
            Record(
                raw_data={
                    "@admin": {
                        "id": "F123456789",
                    },
                    "identifier": [
                        {
                            "faid": "F123456789",
                            "primary": True,
                            "type": "faid",
                            "value": "F123456789",
                        },
                    ],
                }
            ),
            "https://discovery.nationalarchives.gov.uk/details/c/F123456789",
        ),
        (
            "NRA",
            Record(
                raw_data={
                    "source": {"value": "NRA"},
                    "@template": {
                        "details": {
                            "iaid": "N13634630",
                        }
                    },
                },
            ),
            "https://discovery.nationalarchives.gov.uk/details/r/N13634630",
        ),
        (
            "MYC",
            Record(
                raw_data={
                    "source": {"value": "MYC"},
                    "@template": {
                        "details": {
                            "iaid": "efc75381-8a4c-4810-9e2f-340c3038ddc9",
                        }
                    },
                }
            ),
            "https://discovery.nationalarchives.gov.uk/details/r/efc75381-8a4c-4810-9e2f-340c3038ddc9",
        ),
        (
            "DRI",
            Record(
                raw_data={
                    "source": {"value": "CAT"},
                    "@template": {
                        "details": {
                            "iaid": "00149557ca64456a8a41e44f14621801_1",
                        }
                    },
                }
            ),
            "https://discovery.nationalarchives.gov.uk/details/r/00149557ca64456a8a41e44f14621801_1",
        ),
    ]

    def test_default(self):
        for attribute_name, expected_result in (
            ("record_instance", "/catalogue/ref/2515/300/1/"),
            (
                "record_instance_no_reference",
                "/catalogue/id/e7e92a0b-3666-4fd6-9dac-9d9530b0888c/",
            ),
            (
                "interpretive_record",
                "https://www.example.com",
            ),
        ):
            with self.subTest(attribute_name):
                source = getattr(self, attribute_name)

                self.assertEqual(
                    record_url(source, is_editorial=False), expected_result
                )
                # is_editorial should't make a difference unless
                # FEATURE_RECORD_LINKS_GO_TO_DISCOVERY is True
                self.assertEqual(record_url(source, is_editorial=True), expected_result)

    @override_settings(FEATURE_RECORD_LINKS_GO_TO_DISCOVERY=True)
    def test_discovery_links_when_is_editorial_is_true(self):
        for attribute_name, expected_result in (
            (
                "record_instance",
                "https://discovery.nationalarchives.gov.uk/details/r/e7e92a0b-3666-4fd6-9dac-9d9530b0888c",
            ),
            (
                "record_instance_no_reference",
                "https://discovery.nationalarchives.gov.uk/details/r/e7e92a0b-3666-4fd6-9dac-9d9530b0888c",
            ),
            (
                "interpretive_record",
                "https://www.example.com",
            ),
        ):
            with self.subTest(attribute_name):
                source = getattr(self, attribute_name)
                self.assertEqual(record_url(source, is_editorial=True), expected_result)

    @override_settings(FEATURE_RECORD_LINKS_GO_TO_DISCOVERY=True)
    def test_no_discovery_links_when_is_editorial_is_false(self):
        for attribute_name, expected_result in (
            ("record_instance", "/catalogue/ref/2515/300/1/"),
            (
                "record_instance_no_reference",
                "/catalogue/id/e7e92a0b-3666-4fd6-9dac-9d9530b0888c/",
            ),
            (
                "interpretive_record",
                "https://www.example.com",
            ),
        ):
            with self.subTest(attribute_name):
                source = getattr(self, attribute_name)
                self.assertEqual(
                    record_url(source, is_editorial=False), expected_result
                )

    def test_discovery_link_for_various_records(self):
        for iaid_format, record, expected_result in self.records_various:
            with self.subTest(iaid_format):
                self.assertEqual(
                    record_url(record, order_from_discovery=True), expected_result
                )

    def test_repository_links(self):
        for attribute_name, expected_result in (
            ("record_instance", "/catalogue/ref/66/"),
            ("record_instance_no_reference", ""),
        ):
            with self.subTest(attribute_name):
                source = getattr(self, attribute_name)
                self.assertEqual(record_url(source.repository), expected_result)

    def test_non_reference_number_url(self):
        # tests using raw source
        for attribute_name, expected_result in (
            ("record_instance", "/catalogue/id/e7e92a0b-3666-4fd6-9dac-9d9530b0888c/"),
            (
                "record_instance_no_reference",
                "/catalogue/id/e7e92a0b-3666-4fd6-9dac-9d9530b0888c/",
            ),
        ):
            with self.subTest(attribute_name):
                source = getattr(self, attribute_name)
                self.assertEqual(
                    record_url(source, use_non_reference_number_url=True),
                    expected_result,
                )

        # tests using repository attribute
        for attribute_name, expected_result in (
            ("record_instance", "/catalogue/id/A13531109/"),
            ("record_instance_no_reference", ""),
        ):
            with self.subTest(attribute_name):
                source = getattr(self, attribute_name)
                self.assertEqual(
                    record_url(source.repository, use_non_reference_number_url=True),
                    expected_result,
                )

    def test_is_page_current_item_in_hierarchy(self):
        page = self.tna_long_hierarchy_record_instance
        hierarchy = page.hierarchy
        for name, level_item, expected_result in (
            ("item_level_1", hierarchy[0], False),
            ("item_level_3", hierarchy[1], False),
            ("item_level_6", hierarchy[2], False),
            ("item_level_7", hierarchy[3], True),
        ):
            with self.subTest(name):
                self.assertEqual(
                    is_page_current_item_in_hierarchy(page, level_item), expected_result
                )

    def test_level_name(self):
        for current_record, expected_result in (
            (self.tna_record_instance, "Series"),
            (self.record_instance, "Sub-fonds"),
        ):
            with self.subTest(self):
                # We pass in the current record level code and is_tna value
                # and this function then retrieves the level name associated
                # with that level code/record
                self.assertEqual(
                    level_name(current_record.level_code, current_record.is_tna),
                    expected_result,
                )

    def test_breadcrumb_items(self):
        tna_record = self.tna_long_hierarchy_record_instance
        tna_hierarchy = tna_record.hierarchy
        other_record = self.long_hierarchy_record_instance
        other_hierarchy = other_record.hierarchy
        for current_record, expected_result in (
            (tna_record, [tna_hierarchy[0], tna_hierarchy[1], tna_record]),
            (
                other_record,
                [
                    other_hierarchy[1],
                    other_hierarchy[2],
                    other_record,
                ],
            ),
        ):
            with self.subTest(self):
                # We pass in the record hierarchy, is_tna value and the current record
                # and this function then retrieves the breadcrumb items associated
                # with that hierarchy, depending on the state of is_tna
                self.assertEqual(
                    breadcrumb_items(
                        current_record.hierarchy, current_record.is_tna, current_record
                    ),
                    expected_result,
                )

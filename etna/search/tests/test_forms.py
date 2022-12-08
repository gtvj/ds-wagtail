from django.test import SimpleTestCase

from ..forms import CatalogueSearchForm


class CatalogueSearchFormTest(SimpleTestCase):
    def test_various_opening_date_inputs_is_valid(self):
        """tests inputs accross both date fields with various input formats for form validity"""
        for label, form_data in (
            (
                "input end date with empty start date",
                {
                    "group": "tna",
                    "opening_end_date_0": "01",
                    "opening_end_date_1": "01",
                    "opening_end_date_2": "2000",
                },
            ),
            (
                "input start date with empty end date",
                {
                    "group": "tna",
                    "opening_start_date_0": "31",
                    "opening_start_date_1": "12",
                    "opening_start_date_2": "1999",
                },
            ),
            (
                "input start date before end date",
                {
                    "group": "tna",
                    "opening_start_date_0": "31",
                    "opening_start_date_1": "12",
                    "opening_start_date_2": "1999",
                    "opening_end_date_0": "01",
                    "opening_end_date_1": "01",
                    "opening_end_date_2": "2000",
                },
            ),
            (
                "input for day - start date and end date are same",
                {
                    "group": "tna",
                    "opening_start_date_0": "31",
                    "opening_start_date_1": "12",
                    "opening_start_date_2": "1999",
                    "opening_end_date_0": "31",
                    "opening_end_date_1": "12",
                    "opening_end_date_2": "1999",
                },
            ),
        ):
            with self.subTest(label):
                form = CatalogueSearchForm(form_data)
                self.assertTrue(form.is_valid(), label)

    def test_opening_start_date_before_opening_end_date_is_invalid(self):
        """tests inputs accross both date fields for form invalidity"""

        for label, form_data in (
            (
                "input start date after end date with all fields input DDMMYYY",
                {
                    "group": "tna",
                    "opening_start_date_0": "01",
                    "opening_start_date_1": "01",
                    "opening_start_date_2": "2000",
                    "opening_end_date_0": "31",
                    "opening_end_date_1": "12",
                    "opening_end_date_2": "1999",
                },
            ),
            (
                "input start date after end date with partial fields input YYYY",
                {
                    "group": "tna",
                    "opening_start_date_2": "2000",
                    "opening_end_date_2": "1999",
                },
            ),
            (
                "input start date after end date with partial fields input MMYYYY",
                {
                    "group": "tna",
                    "opening_start_date_1": "01",
                    "opening_start_date_2": "2000",
                    "opening_end_date_1": "12",
                    "opening_end_date_2": "1999",
                },
            ),
        ):
            with self.subTest(label):
                form = CatalogueSearchForm(form_data)
                self.assertFalse(form.is_valid(), label)
                self.assertEqual(
                    form.errors.get("opening_start_date", None),
                    ["There is a problem. Start date cannot be after end date"],
                )

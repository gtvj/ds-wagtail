from django.test import SimpleTestCase

from ..forms import CatalogueSearchForm


class CatalogueSearchFormTest(SimpleTestCase):
    def test_various_opening_date_inputs_is_valid(self):
        """tests inputs accross both date fields with various input formats for form validity"""
        for label, value in (
            (
                "input end date with empty start date",
                {
                    "input": {
                        "group": "tna",
                        "opening_end_date_0": "01",
                        "opening_end_date_1": "01",
                        "opening_end_date_2": "2000",
                    }
                },
            ),
            (
                "input start date with empty end date",
                {
                    "input": {
                        "group": "tna",
                        "opening_start_date_0": "31",
                        "opening_start_date_1": "12",
                        "opening_start_date_2": "1999",
                    }
                },
            ),
            (
                "input start date before end date",
                {
                    "input": {
                        "group": "tna",
                        "opening_start_date_0": "31",
                        "opening_start_date_1": "12",
                        "opening_start_date_2": "1999",
                        "opening_end_date_0": "01",
                        "opening_end_date_1": "01",
                        "opening_end_date_2": "2000",
                    }
                },
            ),
            (
                "input for day - start date and end date are same",
                {
                    "input": {
                        "group": "tna",
                        "opening_start_date_0": "31",
                        "opening_start_date_1": "12",
                        "opening_start_date_2": "1999",
                        "opening_end_date_0": "31",
                        "opening_end_date_1": "12",
                        "opening_end_date_2": "1999",
                    }
                },
            ),
        ):
            with self.subTest(label):
                form = CatalogueSearchForm(value["input"])
                self.assertTrue(form.is_valid(), label)

    def test_opening_start_date_before_opening_end_date_is_invalid(self):
        """tests inputs accross both date fields for form invalidity"""
        form = CatalogueSearchForm(
            {
                "group": "tna",
                "opening_start_date_0": "01",
                "opening_start_date_1": "01",
                "opening_start_date_2": "2000",
                "opening_end_date_0": "31",
                "opening_end_date_1": "12",
                "opening_end_date_2": "1999",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.get("opening_start_date", None),
            ["Start date cannot be after end date"],
        )

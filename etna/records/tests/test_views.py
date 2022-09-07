import io
import re
import unittest

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from wagtail.models import Group
from wagtail.tests.utils import WagtailTestUtils

import responses

from etna.core.test_utils import prevent_request_warnings

from ...ciim.tests.factories import create_media, create_record, create_response

User = get_user_model()


class TestRecordDisambiguationView(TestCase):
    @responses.activate
    @prevent_request_warnings
    def test_no_matches_respond_with_404(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/searchUnified",
            json=create_response(records=[]),
        )

        response = self.client.get("/catalogue/ref/AD/2/2/")

        self.assertEquals(
            response.resolver_match.view_name, "details-page-human-readable"
        )
        self.assertEquals(response.status_code, 404)

    @responses.activate
    def test_disambiguation_page_rendered_for_multiple_results(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/searchUnified",
            json=create_response(
                records=[
                    create_record(reference_number="ADM 223/3"),
                    create_record(reference_number="ADM 223/3"),
                ]
            ),
        )

        response = self.client.get("/catalogue/ref/ADM/223/3/")

        self.assertEquals(
            response.resolver_match.view_name, "details-page-human-readable"
        )
        self.assertTemplateUsed(response, "records/record_disambiguation_page.html")

    @responses.activate
    def test_rendering_deferred_to_details_page_view(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/searchUnified",
            json=create_response(
                records=[
                    create_record(iaid="C123456", reference_number="ADM 223/3"),
                ]
            ),
        )

        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", reference_number="ADM 223/3"),
                ]
            ),
        )

        response = self.client.get("/catalogue/ref/ADM/223/3/", follow=False)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.resolver_match.view_name, "details-page-human-readable"
        )
        self.assertTemplateUsed(response, "records/record_detail.html")


class TestRecordView(TestCase):
    @responses.activate
    @prevent_request_warnings
    def test_no_matches_respond_with_404(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(records=[]),
        )

        response = self.client.get("/catalogue/id/C123456/")

        self.assertEquals(response.status_code, 404)
        self.assertEquals(
            response.resolver_match.view_name, "details-page-machine-readable"
        )

    @responses.activate
    def test_record_rendered_for_single_result(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456"),
                ]
            ),
        )

        response = self.client.get("/catalogue/id/C123456/")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.resolver_match.view_name, "details-page-machine-readable"
        )
        self.assertTemplateUsed(response, "records/record_detail.html")

    @unittest.skip(
        "Kong open beta API does not support media. Re-enable/update once media is available."
    )
    @responses.activate
    def test_record_renders_for_record_with_no_image(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=True),
                ]
            ),
        )

        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(records=[]),
        )

        response = self.client.get("/catalogue/id/C123456/")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.resolver_match.view_name, "details-page-machine-readable"
        )
        self.assertTemplateUsed(response, "records/record_detail.html")
        self.assertTemplateNotUsed(response, "records/image-viewer-panel.html")

    @unittest.skip(
        "Kong open beta API does not support media. Re-enable/update once media is available."
    )
    @responses.activate
    def test_record_renders_for_record_with_image(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=True),
                ]
            ),
        )

        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(
                records=[
                    create_media(),
                ]
            ),
        )

        responses.add(
            responses.GET,
            "https://kong.test/media",
            body="",
            stream=True,
        )

        response = self.client.get("/catalogue/id/C123456/")

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "records/record_detail.html")
        self.assertTemplateUsed(response, "includes/records/image-viewer-panel.html")


class TestDataLayerRecordDetail(WagtailTestUtils, TestCase):
    @responses.activate
    def test_datalayer_level1(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level1.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C241/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "Held by not available", "customDimension12": "Level 1 - Lettercode", "customDimension13": "", "customDimension14": "RAIL - Records of the pre-nationalisation railway companies, pre-nationalisation canal and...", "customDimension15": "CAT", "customDimension16": "", "customDimension17": ""}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)

    @responses.activate
    def test_datalayer_level2(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level2.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C995/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "Held by not available", "customDimension12": "Level 2 - Division", "customDimension13": "", "customDimension14": "Division within POWE - Records of the Coal Division", "customDimension15": "CAT", "customDimension16": "", "customDimension17": ""}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)

    @responses.activate
    def test_datalayer_level3(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level3.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C12441/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "66 - The National Archives", "customDimension12": "Level 3 - Series", "customDimension13": "", "customDimension14": "RAIL 253 - Great Western Railway Company: Miscellaneous Books and Records", "customDimension15": "CAT", "customDimension16": "", "customDimension17": ""}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)

    @responses.activate
    def test_datalayer_level4(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level4.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C31931/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "Held by not available", "customDimension12": "Level 4 - Sub-series", "customDimension13": "", "customDimension14": "Sub-series within ADM 171 - AFRICA GENERAL SERVICE MEDAL 1902-1910", "customDimension15": "CAT", "customDimension16": "", "customDimension17": ""}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)

    @responses.activate
    def test_datalayer_level5(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level5.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C145033/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "Held by not available", "customDimension12": "Level 5 - Sub-sub-series", "customDimension13": "IR 900 - Specimens of Series of Documents Destroyed", "customDimension14": "Sub-sub-series within IR 900 - Camden Town Tax District", "customDimension15": "CAT", "customDimension16": "", "customDimension17": ""}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)

    @responses.activate
    def test_datalayer_level6_nondigital(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level6_nondigital.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C2361422/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "66 - The National Archives", "customDimension12": "Level 6 - Piece", "customDimension13": "RAIL 253 - Great Western Railway Company: Miscellaneous Books and Records", "customDimension14": "RAIL 253/516 - Correspondence by members of Audit Office, Paddington while on active service to...", "customDimension15": "CAT", "customDimension16": "", "customDimension17": "No availability condition provisioned for this record"}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)

    @responses.activate
    def test_datalayer_level6_digital(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level6_digital.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C198022/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "66 - The National Archives", "customDimension12": "Level 6 - Piece", "customDimension13": "PROB 1 - Prerogative Court of Canterbury: Wills of Selected Famous Persons", "customDimension14": "PROB 1/4 - Will of William Shakespeare 25 March 1616. Proved 22 June 1616.", "customDimension15": "CAT", "customDimension16": "", "customDimension17": "No availability condition provisioned for this record"}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)

    @responses.activate
    def test_datalayer_level7_nondigital(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level7_nondigital.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C6518465/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "66 - The National Archives", "customDimension12": "Level 7 - Item", "customDimension13": "DSIR 27 - Department of Scientific and Industrial Research: Road Research Laboratory Reports", "customDimension14": "DSIR 27/6/ADM171 - The pressures produced by explosions underwater of 1-oz. solid cone charges of P.E....", "customDimension15": "CAT", "customDimension16": "", "customDimension17": "No availability condition provisioned for this record"}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)

    @responses.activate
    def test_datalayer_level7_digital(self):
        import json

        path = f"{settings.BASE_DIR}/etna/records/tests/fixtures/record_level7_digital.json"
        with open(path, "r") as f:
            responses.add(
                responses.GET,
                "https://kong.test/data/fetch",
                json=json.loads(f.read()),
            )

        response = self.client.get("/catalogue/id/C14017032/")

        self.assertTemplateUsed(response, "records/record_detail.html")

        html_decoded_response = response.content.decode("utf8")
        desired_datalayer_script_tag = """<script id="gtmDatalayer" type="application/json">{"contentGroup1": "Catalogue: The National Archives", "customDimension1": "offsite", "customDimension2": "", "customDimension3": "record detail", "customDimension4": "", "customDimension5": "", "customDimension6": "", "customDimension7": "", "customDimension8": "", "customDimension9": "", "customDimension10": "", "customDimension11": "66 - The National Archives", "customDimension12": "Level 7 - Item", "customDimension13": "WO 95 - War Office: First World War and Army of Occupation War Diaries", "customDimension14": "WO 95/1510/4 - Headquarters Branches and Services: General Staff.", "customDimension15": "CAT", "customDimension16": "", "customDimension17": "No availability condition provisioned for this record"}</script>"""
        self.assertIn(desired_datalayer_script_tag, html_decoded_response)


@unittest.skip(
    "Kong open beta API does not support media. Re-enable/update once media is available."
)
class TestImageServeView(TestCase):
    def test_no_location_404s(self):
        response = self.client.get("/records/media/")

        self.assertEquals(response.status_code, 404)

    @responses.activate
    def test_404_response_from_kong_is_forwarded(self):
        responses.add(
            responses.GET,
            re.compile("^https://kong.test/media"),
            status=404,
        )

        response = self.client.get("/records/image/missing/image.jpeg")

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.resolver_match.url_name, "image-serve")

    @responses.activate
    def test_success(self):
        responses.add(
            responses.GET,
            re.compile("^https://kong.test/media"),
            body=io.BufferedReader(io.BytesIO(b"test byte stream")),
            content_type="application/octet-stream",
            stream=True,
        )

        response = self.client.get("/records/image/valid/path.jpg")

        self.assertEquals(response["content-type"], "image/jpeg")
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.streaming)


@unittest.skip(
    "Kong open beta API does not support media. Re-enable/update once media is available."
)
class TestImageBrowseView(TestCase):
    @responses.activate
    def test_image_browse_non_digitised_record(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=False),
                ]
            ),
        )
        response = self.client.get("/records/images/C123456/")

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.resolver_match.url_name, "image-browse")

    @responses.activate
    def test_image_browse_record_with_no_media(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(
                        iaid="C123456", is_digitised=True, media_reference_id=None
                    ),
                ]
            ),
        )
        response = self.client.get("/records/images/C123456/")

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.resolver_match.url_name, "image-browse")

    @responses.activate
    def test_success(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=True),
                ]
            ),
        )
        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(
                records=[
                    create_media(),
                ]
            ),
        )
        responses.add(
            responses.GET,
            "https://kong.test/media",
            body="",
            stream=True,
        )

        response = self.client.get("/records/images/C123456/")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.resolver_match.url_name, "image-browse")


@unittest.skip(
    "Kong open beta API does not support media. Re-enable/update once media is available."
)
class TestImageViewerView(TestCase):
    def setUp(self):
        private_beta_user = User(
            username="private-beta@email.com", email="private-beta@email.com"
        )
        private_beta_user.set_password("password")
        private_beta_user.save()
        private_beta_user.groups.add(Group.objects.get(name="Beta Testers"))

        self.client.login(email="private-beta@email.com", password="password")

    @responses.activate
    def test_image_browse_non_digitised_record(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=False),
                ]
            ),
        )
        response = self.client.get("/records/images/C123456/01/")

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.resolver_match.url_name, "image-viewer")

    @responses.activate
    def test_image_browse_record_with_no_media(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(
                        iaid="C123456", is_digitised=True, media_reference_id=None
                    ),
                ]
            ),
        )
        response = self.client.get("/records/images/C123456/01/")

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.resolver_match.url_name, "image-viewer")

    @responses.activate
    def test_success(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=True),
                ]
            ),
        )
        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(
                records=[
                    create_media(location="path/to/previous-image.jpeg", sort="01"),
                    create_media(location="path/to/image.jpeg", sort="02"),
                    create_media(location="path/to/next-image.jpeg", sort="03"),
                ]
            ),
        )
        responses.add(
            responses.GET,
            "https://kong.test/media",
            body="",
            stream=True,
        )

        response = self.client.get("/records/images/C123456/02/")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.resolver_match.url_name, "image-viewer")
        self.assertEquals(
            response.context["previous_image"].location, "path/to/previous-image.jpeg"
        )
        self.assertEquals(response.context["image"].location, "path/to/image.jpeg")
        self.assertEquals(
            response.context["next_image"].location, "path/to/next-image.jpeg"
        )

    @responses.activate
    def test_no_next_image(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=True),
                ]
            ),
        )
        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(
                records=[
                    create_media(location="path/to/previous-image.jpeg", sort="01"),
                    create_media(location="path/to/image.jpeg", sort="02"),
                ]
            ),
        )

        response = self.client.get("/records/images/C123456/02/")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.resolver_match.url_name, "image-viewer")
        self.assertEquals(
            response.context["previous_image"].location, "path/to/previous-image.jpeg"
        )
        self.assertEquals(response.context["image"].location, "path/to/image.jpeg")
        self.assertEquals(response.context["next_image"], None)

    @responses.activate
    def test_no_previous_image(self):
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=True),
                ]
            ),
        )
        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(
                records=[
                    create_media(location="path/to/image.jpeg", sort="01"),
                    create_media(location="path/to/next-image.jpeg", sort="02"),
                ]
            ),
        )

        response = self.client.get("/records/images/C123456/01/")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.resolver_match.url_name, "image-viewer")
        self.assertEquals(response.context["previous_image"], None)
        self.assertEquals(response.context["image"].location, "path/to/image.jpeg")
        self.assertEquals(
            response.context["next_image"].location, "path/to/next-image.jpeg"
        )

    @responses.activate
    def test_previous_image_but_no_selected_image(self):
        """Modifying the URL to attempt to display image_count + 1 image should 404."""

        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=True),
                ]
            ),
        )
        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json=create_response(
                records=[
                    create_media(location="path/to/previous-image.jpeg", sort="01"),
                ]
            ),
        )

        response = self.client.get("/records/images/C123456/02/")

        self.assertEquals(response.status_code, 404)

    @responses.activate
    def test_invalid_response_from_kong_raises_404(self):
        """It's possible for us to pass a very long offset to Kong that returns a 400.

        In such an event, ensure that we gracefully handle the error."""
        responses.add(
            responses.GET,
            "https://kong.test/data/fetch",
            json=create_response(
                records=[
                    create_record(iaid="C123456", is_digitised=True),
                ]
            ),
        )
        responses.add(
            responses.GET,
            "https://kong.test/data/search",
            json={
                "timestamp": "2021-08-26T09:07:31.688+00:00",
                "status": 400,
                "error": "Bad Request",
                "message": """
                  Failed to convert value of type 'java.lang.String' to required type 'java.lang.Integer';
                  nested exception is java.lang.NumberFormatException: For input string: \"999999999999999999\"
                  """,
                "path": "/search",
            },
            status=400,
        )

        response = self.client.get("/records/images/C123456/11000000000000000000/")

        self.assertEquals(response.status_code, 404)

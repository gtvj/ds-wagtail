import urllib

from datetime import date

from django.test import RequestFactory, TestCase
from django.utils import timezone

from etna.home.factories import HomePageFactory

from ..factories import EventPageFactory, WhatsOnPageFactory
from ..models import AudienceType, EventAudienceType, EventSession, EventType


class TestWhatsOnPageEventFiltering(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.home_page = HomePageFactory()

        cls.whats_on_page = WhatsOnPageFactory(title="What's On", parent=cls.home_page)

        cls.tour_event_type = EventType(
            name="Tour",
            slug="tour",
        )
        cls.tour_event_type.save()

        cls.talk_event_type = EventType(
            name="Talk",
            slug="talk",
        )
        cls.talk_event_type.save()

        cls.family_audience_type = AudienceType(
            name="Families",
            slug="families",
        )
        cls.family_audience_type.save()

        cls.event_audience_type = EventAudienceType(
            page=cls.whats_on_page,
            audience_type=cls.family_audience_type,
        )
        cls.event_audience_type.save()

        cls.event_page1 = EventPageFactory(
            title="Event page 1",
            parent=cls.whats_on_page,
            event_type=cls.talk_event_type,
            venue_type="online",
            min_price=0,
            max_price=0,
            start_date=timezone.datetime(2023, 10, 17),
            sessions=[
                EventSession(
                    page=cls.whats_on_page,
                    start=timezone.datetime(2023, 10, 15),
                    end=timezone.datetime(2023, 10, 16),
                )
            ],
        )

        cls.event_page2 = EventPageFactory(
            title="Event page 2",
            parent=cls.whats_on_page,
            event_type=cls.talk_event_type,
            event_audience_types=[cls.event_audience_type],
            venue_type="online",
            min_price=0,
            max_price=15,
            start_date=timezone.datetime(2023, 10, 17),
            sessions=[
                EventSession(
                    page=cls.whats_on_page,
                    start=timezone.datetime(2023, 10, 17),
                    end=timezone.datetime(2023, 10, 18),
                )
            ],
        )

        cls.event_page3 = EventPageFactory(
            title="Event page 3",
            parent=cls.whats_on_page,
            event_type=cls.tour_event_type,
            venue_type="in_person",
            min_price=15,
            max_price=30,
            start_date=timezone.datetime(2023, 10, 20),
            sessions=[
                EventSession(
                    page=cls.whats_on_page,
                    start=timezone.datetime(2023, 10, 20),
                    end=timezone.datetime(2023, 10, 21),
                )
            ],
        )

    def test_get_event_pages(self):
        self.assertQuerySetEqual(
            self.whats_on_page.events,
            [self.event_page1, self.event_page2, self.event_page3],
        )

    def assert_filtered_event_pages_equal(self, filter_params, expected_result):
        self.assertQuerySetEqual(
            self.whats_on_page.filter_events(filter_params), expected_result
        )

    def test_filtered_event_pages(self):
        test_cases = (
            ({}, [self.event_page1, self.event_page2, self.event_page3]),
            ({"is_online_event": True}, [self.event_page1, self.event_page2]),
            (
                {"event_type": self.talk_event_type},
                [self.event_page1, self.event_page2],
            ),
            ({"event_type": self.tour_event_type}, [self.event_page3]),
            ({"family_friendly": True}, [self.event_page2]),
            ({"date": date(2023, 10, 20)}, [self.event_page3]),
        )

        for filter_params, expected in test_cases:
            with self.subTest(filter_params=filter_params, expected=expected):
                self.assert_filtered_event_pages_equal(filter_params, expected)

    def test_price_range(self):
        test_cases = (
            (self.event_page1.price_range, "Free"),
            (self.event_page2.price_range, "Free - 15"),
            (self.event_page3.price_range, "15 - 30"),
        )

        for test_value, expected in test_cases:
            with self.subTest(test_value=test_value, expected=expected):
                self.assertEqual(test_value, expected)

    def test_remove_filter_urls(self):
        """
        The URL we generate to remove a filter from the listing should not include that field
        """
        query_dict = {
            "date": "2023-10-03",
            "event_type": self.talk_event_type.id,
            "is_online_event": "on",
            "family_friendly": "on",
        }
        query_string = urllib.parse.urlencode(query_dict)
        request_url = f"/?{query_string}"
        request = RequestFactory().get(request_url)

        for field_name in query_dict.keys():
            with self.subTest(field_name=field_name):
                url_parts = urllib.parse.urlparse(
                    self.whats_on_page.build_unset_filter_url(request, field_name)
                )
                updated_query_dict = urllib.parse.parse_qs(url_parts.query)
                self.assertNotIn(field_name, updated_query_dict)

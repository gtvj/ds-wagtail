import urllib
from datetime import date, datetime
from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.utils import timezone
from django.core.management import call_command
from django.conf import settings

from etna.home.factories import HomePageFactory
from etna.whatson.factories import EventPageFactory, WhatsOnPageFactory
from etna.whatson.models import AudienceType, EventAudienceType, EventSession, EventType, EventPage
from etna.whatson.tna_eventbrite import TNAEventbrite

class TestWhatsOnEventLoader(TestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

        self.events1 = {
                        "events": [
                {
                    "changed": "2023-09-14T19:59:38Z",
                    "created": "2023-03-29T12:41:26Z",
                    "description": {
                        "text": "Join us to view the suffrage movement "
                        "through the lens of the index of "
                        "arrested Suffragettes.",
                    },
                    "end": {
                        "local": "2024-03-15T15:00:00",
                        "timezone": "Europe/London",
                        "utc": "2024-03-15T15:00:00Z",
                    },
                    "format": {
                        "id": "2",
                        "short_name": "Seminar",
                    },
                    "id": "602461046207",
                    "is_series": False,
                    "is_series_parent": False,
                    "listed": True,
                    "name": {
                        "html": "The Index of Suffragettes Arrested",
                        "text": "The Index of Suffragettes Arrested",
                    },
                    "online_event": True,
                    "organization_id": "32190014757",
                    "organizer": {
                        "_type": "organizer",
                        "website": "http://nationalarchives.gov.uk",
                    },
                    "organizer_id": "2226699547",
                    "start": {
                        "utc": "2024-03-15T14:00:00Z",
                    },
                    "status": "live",
                   "summary": "Join us to view the suffrage movement through the "
                    "lens of the index of arrested Suffragettes.",
                    "ticket_classes": [
                        {
                            "cost": {
                                "currency": "GBP",
                                "display": "£5.00",
                                "major_value": "5.00",
                                "value": 500,
                            },
                            "event_id": "602461046207",
                        },
                        {
                            "cost": None,
                            "event_id": "602461046207",
                        },
                        {
                            "cost": {
                                "currency": "GBP",
                                "display": "£10.00",
                                "major_value": "10.00",
                                "value": 1000,
                            },
                            "event_id": "602461046207",
                        },
                        {
                            "cost": {
                                "currency": "GBP",
                                "display": "£15.00",
                                "major_value": "15.00",
                                "value": 1500,
                            },
                            "event_id": "602461046207",
                        },
                    ],
                    "tx_time_limit": 480,
                    "url": "https://www.eventbrite.co.uk/e/the-index-of-suffragettes-arrested-tickets-602461046207",
                    "venue": None,
                    "venue_id": None,
                    "version": None,
                },
            ],
            "pagination": {
                "has_more_items": False,
                "object_count": 1,
                "page_count": 1,
                "page_number": 1,
                "page_size": 200,
            },
        }

        self.event_description1 = {'description': '<div>Join us to view the suffrage movement through the lens of the index of arrested Suffragettes.</div><div style="margin-top: 20px"><div style="margin: 20px 10px;font-size: 15px;line-height: 22px;font-weight: 400;text-align: left;"><p>At the turn of the twentieth century, Votes for women was one of the biggest domestic political issues of the day. Suffrage supporters, frustrated with the lack of progress, turned to increasingly militant methods, from heckling politicians to arson attacks. The government was constantly struggling to keep up with their innovative, evolving campaigns. In response, the Home Office created an index of arrested Suffragettes to keep tabs on the activities of individuals, record aliases and link convictions.</p><p>Through this single iconic document, it is possible to gain an insight into a vibrant national movement. It records the leaders of the movement, alongside the everyday foot soldiers who were the backbone of suffrage activism. The index contains 1333 names; 1224 women and 109 men, all arrested in the name of votes for women. Join us to view the suffrage movement through the lens of this record that challenges what we know about the Suffragettes with Diverse Histories Specialist, Vicky Iglikowski-Broad.</p><p><em>Secrets of The National Archives is a new monthly series showcasing some of the most notable documents and tales from our collection. Each month, delve into the fascinating stories behind the documents and learn straight from the experts.</em></p><p><em>From iconic documents such as Magna Carta and Domesday, to our hidden gems, discover The National Archives’ unique and rich collection and explore history as it really happened.  </em></p><p></p></div><div style="margin: 20px 10px;font-size: 15px;line-height: 22px;font-weight: 400;text-align: left;"><p><strong>What’s Online</strong> is a series of talks, in conversation events and webinars delivered by our experts and special guests. Events last approximately one hour, including an audience Q&A. </p><p>This event will be presented on Zoom. For the best experience we recommend using either a laptop or desktop computer.  For more information on attending a Zoom event, please visit: https://bit.ly/3fojVtn </p><p>You will receive a reminder email, including a link to join in advance of the event. </p><p>Talks are available to watch on catch-up for a limited period of 48 hours only. You will receive a separate link to view the recording once the event is over.</p></div><div style="margin: 20px 0;line-height: 22px;"><img src="https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F480385669%2F1061130206503%2F1%2Foriginal.20230329-124734?h=2000&w=720&auto=format%2Ccompress&q=75&sharp=10&s=4387c7410d53cf3e9a3c4b7d7ad800aa" alt="" style="max-width: 100%; height: auto" /></div></div>'}

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

        cls.featured_event = EventPageFactory(
            title="Event page 1",
            parent=cls.whats_on_page,
            event_type=cls.talk_event_type,
            venue_type="online",
            min_price=0,
            max_price=0,
            start_date=timezone.make_aware(datetime(2023, 10, 17)),
        )

        cls.featured_event.sessions = [
            EventSession(
                page=cls.featured_event,
                start=timezone.make_aware(datetime(2023, 10, 15)),
                end=timezone.make_aware(datetime(2023, 10, 16)),
            )
        ]

        cls.whats_on_page.featured_event = cls.featured_event
        cls.featured_event.save()

        cls.event_page_2 = EventPageFactory(
            title="Event page 2",
            parent=cls.whats_on_page,
            event_type=cls.talk_event_type,
            event_audience_types=[cls.event_audience_type],
            venue_type="online",
            min_price=0,
            max_price=15,
            start_date=timezone.make_aware(datetime(2023, 10, 17)),
        )

        cls.event_page_2.sessions = [
            EventSession(
                page=cls.event_page_2,
                start=timezone.make_aware(datetime(2023, 10, 17)),
                end=timezone.make_aware(datetime(2023, 10, 18)),
            )
        ]

        cls.event_page_2.save()

        cls.event_page_3 = EventPageFactory(
            title="Event page 3",
            parent=cls.whats_on_page,
            event_type=cls.tour_event_type,
            venue_type="in_person",
            min_price=15,
            max_price=30,
            start_date=timezone.make_aware(datetime(2023, 10, 20)),
        )

        cls.event_page_3.sessions = [
            EventSession(
                page=cls.event_page_3,
                start=timezone.make_aware(datetime(2023, 10, 20)),
                end=timezone.make_aware(datetime(2023, 10, 21)),
            )
        ]

        cls.event_page_3.save()

        cls.event_page_4 = EventPageFactory(
            title="Event page 4",
            parent=cls.whats_on_page,
            event_type=cls.tour_event_type,
            venue_type="in_person",
            min_price=15,
            max_price=30,
            start_date=timezone.make_aware(datetime(2023, 10, 20)),
        )

        cls.event_page_4.sessions = [
            EventSession(
                page=cls.event_page_4,
                start=timezone.make_aware(datetime(2023, 10, 20, 10, 30)),
                end=timezone.make_aware(datetime(2023, 10, 20, 20, 30)),
            )
        ]

        cls.event_page_4.save()

        cls.event_page_5 = EventPageFactory(
            title="Event page 5",
            parent=cls.whats_on_page,
            event_type=cls.tour_event_type,
            venue_type="in_person",
            min_price=15,
            max_price=30,
            start_date=timezone.make_aware(datetime(2023, 10, 22)),
        )

        cls.event_page_5.sessions = [
            EventSession(
                page=cls.event_page_5,
                start=timezone.make_aware(datetime(2023, 10, 22, 10, 30)),
                end=timezone.make_aware(datetime(2023, 10, 22, 10, 30)),
            )
        ]

        cls.event_page_5.save()

        cls.event_page_6 = EventPageFactory(
            title="Event page 6",
            parent=cls.whats_on_page,
            event_type=cls.tour_event_type,
            venue_type="in_person",
            min_price=15,
            max_price=30,
            start_date=timezone.make_aware(datetime(2023, 10, 22)),
        )

        cls.event_page_6.sessions = [
            EventSession(
                page=cls.event_page_6,
                start=timezone.make_aware(datetime(2023, 10, 22, 10, 30)),
                end=timezone.make_aware(datetime(2023, 10, 22, 11, 30)),
            ),
            EventSession(
                page=cls.event_page_6,
                start=timezone.make_aware(datetime(2023, 10, 22, 11, 30)),
                end=timezone.make_aware(datetime(2023, 10, 22, 12, 30)),
            ),
        ]

        cls.event_page_6.save()

    @patch("etna.whatson.tna_eventbrite.TNAEventbrite.get_event_list")
    @patch("etna.whatson.tna_eventbrite.TNAEventbrite.get_description")
    def test_event_loaded(self, mock_get_description, mock_get_event_list):
        """
        An event has been loaded, with id 602461046207
        """
        mock_get_event_list.return_value = self.events1
        mock_get_description.return_value = self.event_description1

        call_command("event_loader")

        result = EventPage.objects.filter(eventbrite_id='602461046207').values('intro')

        for instance in result:
            self.assertEqual(instance['intro'], "Join us to view the suffrage movement through the lens of the index of arrested Suffragettes.")


    def test_environment_variables_exists(self):
        self.assertIsNotNone(settings.EVENTBRITE_ORGANIZER_ID)
        self.assertIsNotNone(settings.EVENTBRITE_PRIVATE_TOKEN)
        self.assertIsNotNone(settings.EVENTBRITE_TNA_ORGANISATION_ID)

    @patch("etna.whatson.tna_eventbrite.TNAEventbrite.get_event_list")
    @patch("etna.whatson.tna_eventbrite.TNAEventbrite.get_description")
    def test_no_api_response(self, mock_get_description, mock_get_event_list):
        mock_get_event_list.return_value = None
        mock_get_description.return_value = None

        with self.assertRaises(TypeError):
            call_command("event_loader")


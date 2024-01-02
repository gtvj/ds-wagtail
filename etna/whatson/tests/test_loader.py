import urllib
from datetime import date, datetime
from unittest.mock import patch

from django.test import TestCase
from django.core.management import call_command
from django.conf import settings

from etna.home.factories import HomePageFactory
from etna.whatson.factories import WhatsOnPageFactory
from etna.whatson.models import EventPage
from etna.whatson.tna_eventbrite import TNAEventbrite

class TestWhatsOnEventLoader(TestCase):
    def setUp(self):
        super().setUp()

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

    @patch("etna.whatson.tna_eventbrite.TNAEventbrite.get_event_list")
    @patch("etna.whatson.tna_eventbrite.TNAEventbrite.get_description")
    def test_no_api_response(self, mock_get_description, mock_get_event_list):
        mock_get_event_list.return_value = None
        mock_get_description.return_value = None

        with self.assertRaises(TypeError):
            call_command("event_loader")


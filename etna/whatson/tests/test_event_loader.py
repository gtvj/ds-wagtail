import urllib

from datetime import date, datetime

from django.test import RequestFactory, TestCase
from django.utils import timezone

from unittest.mock import patch

from ..factories import EventPageFactory, WhatsOnPageFactory
from ..models import AudienceType, EventAudienceType, EventSession, EventType, EventPage

class TestWhatsOnAPIEventLoader(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
        
    @patch('whatson.tna_eventbrite.TNAEventBrite')
    def xtest_successful_api_request(self, mock_tna_eventbrite):
        # Mock the TNAEventBrite class
        mock_instance = mock_tna_eventbrite.return_value
        mock_instance.get.return_value = {'key': 'value'}

        # Call the management command
        call_command('event_loader')

        # Assuming your download_data command stores data in a model called YourModel
        # Modify this part according to your actual implementation
        from whatson.models import EventPage

        # Check that the data is stored in the database
        self.assertEqual(EventPage.objects.count(), 1)

        # Optionally, you can check specific attributes of the stored data
        saved_data = EventPage.objects.first()
        self.assertEqual(saved_data.key, 'value')

        # You can also assert other behaviors based on your implementation
        # For example, check if logs were generated or if the command behaved as expected
        # ...

        # Clean up if necessary (assuming YourModel has a delete method)
        saved_data.delete()
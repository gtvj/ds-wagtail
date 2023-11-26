from django.core.management.base import BaseCommand
from django.conf import settings
from etna.whatson.apiutils import *
from etna.whatson.tna_eventbrite import TNAEventbrite
import logging

import pprint

EVENTBRITE_EVENTS_EXPANSION = (
    "category,organizer,venue,format,ticket_classes,event_series"
)

"""
    This management program relies on environment variables:
        EVENTBRITE_ORGANIZER_ID
        EVENTBRITE_PRIVATE_TOKEN
        EVENTBRITE_TNA_ORGANISATION_ID

    If these aren't set, you will get an exception raised when trying to access
    the eventlist and pagination 
"""

class Command(BaseCommand):
    help = "Fetch data from Eventbrite TNA api and store in database"
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "debug",
            type=bool,
            nargs='?',
            default=False,
            help="Log at debug level",
        )

    # Main routine
    def handle(self, *args, **kwargs):
        debug = kwargs.get('debug', False)

        if debug:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Debugging mode enabled")

        eventbrite = TNAEventbrite(settings.EVENTBRITE_PRIVATE_TOKEN)

        try:
            evs = eventbrite.get_event_list(
                organisation_id=settings.EVENTBRITE_TNA_ORGANISATION_ID,
                organiser_id=settings.EVENTBRITE_ORGANIZER_ID,
                expand=EVENTBRITE_EVENTS_EXPANSION,
            )
        except:
            self.logger.exception(
                    f"Exception: Exiting without any updates"
                )
            return False

        # We are expecting a json response with two components: a pagination block and a list of events.
        try:
            eventlist = evs["events"]
            pagination = evs["pagination"]
        except KeyError:
            # Failed to retrieve events due to inaccessibility
            self.logger.exception(
                    f"Exception: Cannot access EventBrite api - check environment. Exiting without any updates"
                )
            return False

        # Get WhatsOn page - this is the root page from which the new event pages 'hang off'
        wop = get_whats_on_page()
        
        # Now loop through the events
        event_count = 0
        while True:
            for event in eventlist:
                event_count += 1

                self.logger.debug(f"Downloading event: {event['id']}; is_series: {event['is_series']}; time last changed: {event['changed']}")

                # For each event, get the following fields - these can't be obtained by using the expand feature unfortunately.
                desc = eventbrite.get_description(event["id"])

                # Save required data in new dictionary
                event_data = populate_event_data(event, desc)

                event_data["event_type"] = get_or_create_event_type(
                    event["format"]["short_name"], event["format"]["id"]
                )

                process_event(event_data, wop)

            # The output is paginated, so we may have to requery the EventBrite api using the pagination key. This may occur a number of times.
            if pagination["has_more_items"]:
                evs = eventbrite.get_event_list(
                    organisation_id=settings.EVENTBRITE_TNA_ORGANISATION_ID,
                    organiser_id=settings.EVENTBRITE_ORGANIZER_ID,
                    continuation=pagination["continuation"],
                    expand=EVENTBRITE_EVENTS_EXPANSION,
                )

                eventlist = evs["events"]
                pagination = evs["pagination"]
            else:
                break

        self.logger.info(
            f"Handled {event_count} events"
        )
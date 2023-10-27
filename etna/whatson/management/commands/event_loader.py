from django.core.management.base import BaseCommand
from django.conf import settings
from etna.whatson.apiutils import *
from etna.whatson.tna_eventbrite import TNAEventbrite

import os

import pprint
from eventbrite import Eventbrite

#EVENTBRITE_PRIVATE_TOKEN = "5NB2D6KB5WI7M4FGA7DW"
#EVENTBRITE_TNA_ORGANISATION_ID = "32190014757"

EVENTBRITE_EVENTS_EXPANSION = "category,organizer,venue,format,ticket_classes,event_series"

#EVENTBRITE_ORGANIZER_ID = os.getenv("EVENTBRITE_ORGANIZER_ID")
#EVENTBRITE_API_BASE_URL = "https://www.eventbriteapi.com/v3/"
#EVENTBRITE_PRIVATE_TOKEN = os.getenv("EVENTBRITE_PRIVATE_TOKEN")
#EVENTBRITE_TNA_ORGANISATION_ID = os.getenv("EVENTBRITE_TNA_ORGANISATION_ID")

# Extend the eventbrite SDK class as it has useful connectivity functionality but doesn't return the data in the format we require.

class Command(BaseCommand):
    help = "Fetch data from Eventbrite TNA api and store in database"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update database. Default is to reset database.",
        )

    def handle(self, *args, **kwargs):
        debug = True

        eventbrite = TNAEventbrite(settings.EVENTBRITE_PRIVATE_TOKEN)

        try:
            evs = eventbrite.get_event_list(
                organisation_id=settings.EVENTBRITE_TNA_ORGANISATION_ID,
                organiser_id=settings.EVENTBRITE_ORGANIZER_ID,
                expand=EVENTBRITE_EVENTS_EXPANSION,
            )

            if debug == 1:
                print(evs.pretty)
        except:
            exit(1)

        # We are expecting a json response with two components: a pagination block and a list of events.
        eventlist = evs["events"]
        pagination = evs["pagination"]

        # Get WhatsOn page
        wop = get_whats_on_page()

        # Temporary test code
        temp_truncate_events(wop)

        # Now loop through the events
        while True:
            for event in eventlist:
                # For each event, get the following fields - these can't be obtained by using the expand feature unfortunately.
                desc = eventbrite.get_description(event["id"])

                # Save required data in new dictionary
                event_data = populate_event_data(event, desc)

                event_data["event_type"] = get_or_create_event_type(
                    event["format"]["short_name"], event["format"]["id"]
                )

                if debug:
                    pprint.pprint(event_data)

                add_or_update_event_page(event_data, wop)

            if pagination["has_more_items"]:
                evs = eventbrite.get_event_list(
                    org_id=settings.EVENTBRITE_TNA_ORGANISATION_ID,
                    continuation=pagination["continuation"],
                    expand=EVENTBRITE_EVENTS_EXPANSION,
                )

                if debug:
                    print(evs.pretty)

                eventlist = evs["events"]
                pagination = evs["pagination"]

                if debug:
                    print(pagination)
            else:
                break

        if debug:
            display_data()

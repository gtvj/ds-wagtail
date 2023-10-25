from django.core.management.base import BaseCommand
import pprint
from ...apiutils import populate_event_data, get_or_create_event_type, add_or_update_event_page, display_data, temp_truncate_events
from ...tna_eventbrite import TNAEventbrite

EVENTBRITE_PRIVATE_TOKEN = "5NB2D6KB5WI7M4FGA7DW"
EVENTBRITE_TNA_ORGANISATION_ID = "32190014757"
EVENTBRITE_EVENTS_EXPANSION = "description,category,organizer,venue,format,ticket_classes,ticket_class_id,ticket_buyer_settings,event_series"
EVENTBRITE_ORGANIZER_ID = "2226699547"
EVENTBRITE_API_BASE_URL = "https://www.eventbriteapi.com/v3/"

# Extend the eventbrite SDK class as it has useful connectivity functionality but doesn't return the data in the format we require.

class Command(BaseCommand):
    help = "Fetch data from Eventbrite TNA api and store in database"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--dry",
            action="store_true",
            help="Don't save to the database, just print data instead",
        )

    def handle(self, *args, **kwargs):
        debug = 1
        dryrun = kwargs["dry"] or None

        try:
            eventbrite = TNAEventbrite(EVENTBRITE_PRIVATE_TOKEN)

            evs = eventbrite.get_event_list(
                organisation_id=EVENTBRITE_TNA_ORGANISATION_ID,
                organiser_id=EVENTBRITE_ORGANIZER_ID,
                expand=EVENTBRITE_EVENTS_EXPANSION,
            )
            if debug == 1:
                print(evs.pretty)
        except:
            pass

        # We are expecting a json response with two components: a pagination block and a list of events.
        eventlist = evs["events"]
        pagination = evs["pagination"]

        # Temporary code for testing
        temp_truncate_events()

        # Now loop through the events
        while True:
            for event in eventlist:
                # For each event, get the following fields - these can't be obtained by using the expand feature unfortunately.
                desc = eventbrite.get_description(event["id"])
                #capacity = eventbrite.get_capacity_tier(event["id"])
                #teams = eventbrite.get_teams(event["id"])
                #questions = eventbrite.get_questions(event["id"])

                # Save required data in new dictionary
                event_data = populate_event_data(event, desc)

                if event.get('series_id', False):
                    es = eventbrite.get_event_series(event['series_id'])
                    print(f"Event Series: [{es.pretty}]")

                event_data["event_type"] = get_or_create_event_type(
                    event["format"]["short_name"], event["format"]["id"]
                )
                #event_data["capacity_data"] = populate_capacity_tier(capacity)
                #event_data["team_data"] = populate_teams(teams)
                #event_data["questions"] = populate_questions(questions)

                if debug:
                    pprint.pprint(event_data)
                    print(f"Venue URL: {event_data['venue_website']}")
                    print(f"Event Type: {event['format']['short_name']}")

                add_or_update_event_page(event_data)

            if pagination["has_more_items"]:
                evs = eventbrite.get_event_list(
                    org_id=EVENTBRITE_TNA_ORGANISATION_ID,
                    continuation=pagination["continuation"],
                    expand=EVENTBRITE_EVENTS_EXPANSION,
                )

                if debug == 2:
                    print(evs.pretty)

                eventlist = evs["events"]
                pagination = evs["pagination"]

                if debug:
                    print(pagination)
            else:
                break

        display_data()

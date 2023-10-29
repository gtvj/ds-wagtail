from .models import EventType, EventPage, EventSession, VenueType, WhatsOnPage
from datetime import datetime
from etna.images.models import CustomImage
import re

import pprint as pp


def get_prices_minmax(ticket_classes):
    mintp = 0.0
    maxtp = 0.0

    for tp in ticket_classes:
        if tp.get("cost"):
            if float(tp["cost"]["major_value"]) < mintp:
                mintp = float(tp["cost"]["major_value"])
            if float(tp["cost"]["major_value"]) > maxtp:
                maxtp = float(tp["cost"]["major_value"])
        else:
            mintp = 0.0

    return mintp, maxtp


def populate_event_data(event, event_description):
    pattern = re.compile("<.*?>")
    event_data = {}

    # Remove html
    event_data["full_description"] = re.sub(
        pattern, " ", event_description.get("description")
    )

    event_data["teaser_text"] = (
        event["description"]["text"] if event["description"]["text"] else "Teaser ..."
    )

    event_data["lead_image"] = ""  # CustomImage(title="Unknown")
    event_data["event_type"] = event["format"]["short_name"]

    event_data["series_id"] = event.get("series_id")

    event_data["start_date"] = datetime.strptime(
        event["start"]["utc"], "%Y-%m-%dT%H:%M:%SZ"
    )  #'2024-03-15T14:00:00Z'

    event_data["start_date"] = datetime.fromisoformat(event["start"]["utc"])

    event_data["end_date"] = datetime.strptime(
        event["end"]["utc"], "%Y-%m-%dT%H:%M:%SZ"
    )  #'2024-03-15T14:00:00Z'
    event_data["useful_info"] = ""
    event_data["target_audience"] = ""

    if event["venue"]:  # value always there but may be None
        if not event["online_event"]:
            # Assume that the event is IN_PERSON as there is an address but online event flag is False
            event_data["venue_type"] = VenueType.IN_PERSON
        else:
            # Assume that the event is HYBRID as there is an address and online event flag is True
            event_data["venue_type"] = VenueType.HYBRID

        event_data["venue_website"] = event["organizer"]["website"]
        event_data["venue_address"] = event["venue"]["address"][
            "localized_address_display"
        ]
        event_data["venue_space_name"] = event["venue"]["name"]
    else:
        if not event["online_event"]:
            # Assume that the event is TBA as there is no address and online event flag is False
            event_data["venue_type"] = VenueType.UNKNOWN
        else:
            # Assume that the event is ONLINE as there is no address and online event flag is True
            event_data["venue_type"] = VenueType.ONLINE

        event_data["venue_website"] = ""
        event_data["venue_address"] = ""
        event_data["venue_space_name"] = ""

    event_data["video_conference_info"] = "TBC"
    event_data["registration_url"] = event["url"]

    if event.get("ticket_classes", False):  # value may not be in the dict
        event_data["min_price"], event_data["max_price"] = get_prices_minmax(
            event["ticket_classes"]
        )
    else:
        event_data["min_price"] = 0
        event_data["max_price"] = 0

    event_data["eventbrite_id"] = event["id"]
    event_data["registration_info"] = "TBC"
    event_data["contact_info"] = "TBC"
    event_data["short_title"] = event["name"]["text"][0:50]

    # pp.pprint(event_data)

    return event_data


def populate_capacity_tier(capacity):
    capacity_data = {}

    if capacity:
        capacity_data["total"] = capacity["capacity_total"]
        capacity_data["sold"] = capacity["capacity_sold"]
        capacity_data["pending"] = capacity["capacity_pending"]

    return capacity_data


def populate_teams(teams):
    team_data = {}

    if teams:
        for t in teams["teams"]:
            print(f"Teams is {t}")
            # team_data['name'] = teams.teams[0]['name']

    return team_data


def populate_questions(questions):
    question_data = {}

    if questions:
        print(f"Questions: {questions}")
        # for q in questions:
        #    print(f"Question: {q[0]}")
        # team_data['name'] = teams.teams[0]['name']

    return question_data


def display_data():
    all_events = EventPage.objects.all().values()
    print(f"All Events: {pp.pprint(all_events)}")

    all_sessions = EventSession.objects.all().values()
    print(f"All Sessions: {pp.pprint(all_sessions)}")


def get_or_create_event_type(event_type, event_type_id):
    try:
        obj = EventType.objects.get(name=event_type)
    except EventType.DoesNotExist:
        obj = EventType(name=event_type, slug="Placeholder " + event_type_id)
        obj.save()

    return obj


def get_whats_on_page():
    return WhatsOnPage.objects.first()


def process_event(event, wop):
    ep = add_or_update_event_page(event, wop)
    add_or_update_event_series(ep)


def add_or_update_event_series(parent):
    pass

def test_add_or_update_event_page(event, root_page):

    event_page, created = EventPage.objects.get_or_create(eventbrite_id=event['eventbrite_id'])

    # Populate all mandatory fields from the API
    event_page.description = event["full_description"]
    event_page.useful_info = event["useful_info"]
    event_page.target_audience = event["target_audience"]
    event_page.venue_type = event["venue_type"]
    event_page.venue_website = event["venue_website"]
    event_page.venue_address = event["venue_address"]
    event_page.venue_space_name = event["venue_space_name"]
    event_page.video_conference_info = event["video_conference_info"]
    event_page.registration_url = event["registration_url"]
    event_page.min_price = event["min_price"]
    event_page.max_price = event["max_price"]
    event_page.registration_info = event["registration_info"]
    event_page.contact_info = event["contact_info"]
    event_page.short_title = event["short_title"]
    event_page.event_type = event["event_type"]
    event_page.title = event["short_title"]
    event_page.intro = "Bindi Bhaji"
    event_page.teaser_text = event["teaser_text"]

    # Check if it's not already a child of the root page and update its fields
    if not event_page.is_child_of(root_page):
        # Add the EventPage as a child to the root page
        root_page.add_child(instance=event_page)

    # Save the changes
    event_page.save()

def add_or_update_event_page(event, wop):
    # Given the eventbrite_id, looks to see if it already exists in the database - if it does, then look to update it
    # NOTE: we don't want to override stuff that has been modified by content providers - fix?

    # NOTE: we can't use the ORM update or create because we want treebeard to handle the create.

    ep = EventPage.objects.get(eventbrite_id=event["eventbrite_id"])

    if ep:
        ep.description = event["full_description"]
        ep.useful_info = event["useful_info"]
        ep.target_audience = event["target_audience"]
        ep.venue_type = event["venue_type"]
        ep.venue_website = event["venue_website"]
        ep.venue_address = event["venue_address"]
        ep.venue_space_name = event["venue_space_name"]
        ep.video_conference_info = event["video_conference_info"]
        ep.registration_url = event["registration_url"]
        ep.min_price = event["min_price"]
        ep.max_price = event["max_price"]
        ep.registration_info = event["registration_info"]
        ep.contact_info = event["contact_info"]
        ep.short_title = event["short_title"]
        ep.event_type = event["event_type"]
        ep.title = event["short_title"]
        ep.intro = "Bindi Bhaji"
        ep.teaser_text = event["teaser_text"]
        # Update the page
        ep.save(
            update_fields=[
                "description",
                "useful_info",
                "target_audience",
                "venue_type",
                "venue_website",
                "venue_address",
                "venue_space_name",
                "video_conference_info",
                "registration_url",
                "min_price",
                "max_price",
                "registration_info",
                "contact_info",
                "short_title",
                "event_type",
                "title",
                "intro",
                "teaser_text",
            ]
        )

        return ep

    print(f"Object doesn't exist")
    ep = EventPage(
        description=event["full_description"],
        useful_info=event["useful_info"],
        target_audience=event["target_audience"],
        venue_type=event["venue_type"],
        venue_website=event["venue_website"],
        venue_address=event["venue_address"],
        venue_space_name=event["venue_space_name"],
        video_conference_info=event["video_conference_info"],
        registration_url=event["registration_url"],
        min_price=event["min_price"],
        max_price=event["max_price"],
        eventbrite_id=event["eventbrite_id"],
        registration_info=event["registration_info"],
        contact_info=event["contact_info"],
        short_title=event["short_title"],
        event_type=event["event_type"],
        title=event["short_title"],
        intro="Bindi Bhaji",
        teaser_text=event["teaser_text"],
    )

    series_id = event.get("series_id", None)

    # Otherwise add the child to the database
    wop.add_child(instance=ep)

    return ep

from .models import EventType, EventPage, EventSession, VenueType, WhatsOnPage
from datetime import datetime

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
    event_data = {}

    # Remove html - this will need tweaking in WhatsOn part 2, as it removes href markers that may be of interest
    # It also can result in double spaces.
    event_data["full_description"] = event_description.get("description")

    event_data["teaser_text"] = event["summary"]

    event_data["short_description"] = (
        event["description"]["text"] if event["description"]["text"] else "Intro text ..."
    )

    event_data["lead_image"] = ""
    event_data["event_type"] = event["format"]["short_name"]

    """
    If this event belongs to part of a series, the event['is_series'] will be set to True.
    If this is the case (it is a series), we only save the basic data once with the series id
    instead of the event id.

    In a series, there may be multiple events and the only difference will be the start and end datetimes
    and this is handled further on by the event session table
    """

    event_data["eventbrite_id"] = event["series_id"] if event["is_series"] else event["id"]
    event_data["event_id"] = event["id"] # for the session occurences
    event_data["is_series"] = event["is_series"]
    event_data["need_to_know_button_text"] = ""

    event_data["start_date"] = datetime.strptime(
        event["start"]["utc"], "%Y-%m-%dT%H:%M:%SZ"
    )  #'2024-03-15T14:00:00Z'

    event_data["start_date"] = datetime.fromisoformat(event["start"]["utc"])

    event_data["end_date"] = datetime.strptime(
        event["end"]["utc"], "%Y-%m-%dT%H:%M:%SZ"
    )  #'2024-03-15T14:00:00Z'

    event_data["end_date"] = datetime.fromisoformat(event["end"]["utc"])

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
        
        # Assume that the event is ONLINE as there is no address and online event flag is True
        event_data["venue_type"] = VenueType.ONLINE

        event_data["venue_website"] = ""
        event_data["venue_address"] = ""
        event_data["venue_space_name"] = ""

    event_data["registration_url"] = event["url"]

    if event.get("ticket_classes", False):  # value may not be in the dict
        event_data["min_price"], event_data["max_price"] = get_prices_minmax(
            event["ticket_classes"]
        )
    else:
        event_data["min_price"] = 0
        event_data["max_price"] = 0

    event_data["useful_info"] = ""
    event_data["target_audience"] = ""

    if  event["online_event"]:
        event_data["video_conference_info"] = "TBC"
    else:
        event_data["video_conference_info"] = ""
        
    event_data["registration_info"] = ""
    event_data["contact_info"] = ""

    event_data["short_title"] = event["name"]["text"]

    return event_data

def get_or_create_event_type(event_type, event_type_id):
    try:
        obj = EventType.objects.get(name=event_type)
    except EventType.DoesNotExist:
        obj = EventType(name=event_type, slug="Placeholder " + event_type_id) # Look at slugify()
        obj.save()

    return obj

def get_whats_on_page():
    return WhatsOnPage.objects.first()

def process_event(event, wop):
    event_page = add_or_update_event_page(event, wop)
    add_or_update_event_series(event, event_page)

    # Run the save method on the event_page because event sessions provide the event page minimum and maximum dates.
    event_page.save()

def add_or_update_event_series(event, event_page):
    session_id = event["eventbrite_id"]
    event_id = event["event_id"] if event["is_series"] else None

    try:
        es = EventSession.objects.get(session_id=session_id, event_id=event_id)

        # Potential update for this sessions id
        es.start = event["start_date"]
        es.end = event["end_date"]

        es.save(
            update_fields = [
                "start",
                "end"
            ]
        )

    except EventSession.DoesNotExist:
        EventSession.objects.create(
            page_id = event_page.pk,
            session_id = session_id,
            event_id  = event_id,
            start = event["start_date"],
            end = event["end_date"]
        )

def add_or_update_event_page(event, wop):
    """
        Given the eventbrite_id, looks to see if it already exists in the database - if it does, then look to update it
        NOTE 1: we don't want to override stuff that has been modified by content providers - so we create with more data than 
        we update with.
        NOTE 2: the eventbrite_id is either the event id or the series id if present.
        NOTE 3: we can't use the ORM update or create because we want treebeard to handle the create.
    """

    try:
        ep = EventPage.objects.get(eventbrite_id=event["eventbrite_id"])

        ep.venue_type = event["venue_type"]
        ep.venue_address = event["venue_address"]
        ep.venue_space_name = event["venue_space_name"]
        ep.registration_url = event["registration_url"]
        ep.min_price = event["min_price"]
        ep.max_price = event["max_price"]
        ep.event_type = event["event_type"]
        ep.teaser_text = event["teaser_text"] # Editor - but use a filler text as default

        # Update the page, but only for fields that are not likely to be edited on Wagtail 
        ep.save(
            update_fields=[
                "venue_type",
                "venue_address",
                "venue_space_name",
                "registration_url",
                "min_price",
                "max_price",
                "event_type",
                "teaser_text",
            ]
        )

    except EventPage.DoesNotExist:
        # Insert all available data

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
            short_title=event["short_title"][:50],
            event_type=event["event_type"],
            title=event["short_title"][:50],
            intro=event["short_description"],
            teaser_text=event["teaser_text"],
        )

        # Add the child to the database
        wop.add_child(instance=ep)

    return ep

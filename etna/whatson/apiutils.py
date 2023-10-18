from models import EventType, EventPage, VenueType

# Doesn't work yet!
def get_prices_minmax(ticket_classes):
    mintp = 12345.67
    maxtp = 0.0

    for tp in ticket_classes:
        if tp.get("cost"):
            if float(tp["cost"]["major_value"]) < mintp:
                mintp = float(tp["cost"]["major_value"])
            if float(tp["cost"]["major_value"]) > maxtp:
                maxtp = float(tp["cost"]["major_value"])

    if mintp == 12345.67:
        mintp = 0.0

    return mintp, maxtp


def populate_event_data(event, event_description):
    pattern = re.compile("<.*?>")
    event_data = {}

    event_data["description"] = re.sub(
        pattern, " ", event_description.get("description")
    )

    event_data["lead_image"] = CustomImage(title="Unknown")
    event_data["event_type"] = event["format"]["short_name"]

    event_data["start_date"] = datetime.strptime(
        event["start"]["local"], "%Y-%m-%dT%H:%M:%S"
    )  #'2024-03-15T14:00:00'
    event_data["end_date"] = datetime.strptime(
        event["end"]["local"], "%Y-%m-%dT%H:%M:%S"
    )  #'2024-03-15T14:00:00'
    event_data["useful_info"] = "TBC"
    event_data["target_audience"] = "TBC"

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
            event_data["venue_type"] = VenueType.TBA
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

    event_data["eventbrite_id"] = event["id"]
    event_data["registration_info"] = "TBC"
    event_data["contact_info"] = "TBC"
    event_data["short_title"] = event["name"]["text"]

    print(event_data)

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

    print(f"All Events: {all_events}")


def get_or_create_event_type(event_type, event_type_id):
    try:
        obj = EventType.objects.get(name=event_type)
    except EventType.DoesNotExist:
        obj = EventType(name=event_type, slug="Placeholder " + event_type_id)
        obj.save()

    return obj


def add_or_update_event_page(event):
    ep = EventPage(
        start_date=event["start_date"],
        end_date=event["end_date"],
        description=event["description"],
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
        # The following fields are Wagtail fields and have to be supplied - don't yet know
        # how they will be handled
        event_type=event["event_type"],
        path="PATH",
        title="TITLE",
        depth=1,
        lead_image=event["lead_image"],
        slug=event["eventbrite_id"],
        teaser_text="TEASER",
        intro="INTRO",
    )
    ep.save()

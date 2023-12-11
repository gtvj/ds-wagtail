from eventbrite import Eventbrite

"""
    Extend the supplied EventBrite class becuase that doesn't quite provide us with the functionality we need.
"""

EVENTBRITE_EVENT_STATUS="live,draft,started"
EVENTBRITE_PAGE_SIZE=25

class TNAEventbrite(Eventbrite):
    def __init__(self, authkey):
        super().__init__(authkey)

    def get_event_list(self, organisation_id, organiser_id, continuation=None, **data):
        if continuation:
            return self.get(
                f"/organizations/{organisation_id}/events/?page_size={EVENTBRITE_PAGE_SIZE}&time_filter=current_future&order_by=start_desc&status={EVENTBRITE_EVENT_STATUS}&organizer_filter={organiser_id}&continuation={continuation}",
                data=data,
            )
        else:
            return self.get(
                f"/organizations/{organisation_id}/events/?page_size={EVENTBRITE_PAGE_SIZE}&time_filter=current_future&order_by=start_desc&status={EVENTBRITE_EVENT_STATUS}&organizer_filter={organiser_id}",
                data=data,
            )

    def get_description(self, event_id, **data):
        return self.get(f"/events/{event_id}/description/", data=data)

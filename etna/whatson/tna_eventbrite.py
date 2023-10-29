from eventbrite import Eventbrite


class TNAEventbrite(Eventbrite):
    def __init__(self, authkey):
        super().__init__(authkey)

    def get_event_list(self, organisation_id, organiser_id, continuation=None, **data):

        if continuation:
            # return self.get(f"/organizations/{org_id}/events/?expand.event=organizer,venue&time_filter=current_future&order_by=start_desc&status=live,draft,started&continuation={continuation}", data=data)
            return self.get(
                f"/organizations/{organisation_id}/events/?page_size=200&time_filter=current_future&order_by=start_desc&status=live,draft,started&organizer_filter={organiser_id}&continuation={continuation}",
                # f"/organizations/{organisation_id}/events/?page_size=200&order_by=start_desc&status=draft&organizer_filter={organiser_id}&continuation={continuation}",
                data=data,
            )
        else:
            return self.get(
                f"/organizations/{organisation_id}/events/?page_size=200&time_filter=current_future&order_by=start_desc&status=live,draft,started&organizer_filter={organiser_id}",
                # f"/organizations/{organisation_id}/events/?page_size=200&order_by=start_desc&status=draft&organizer_filter={organiser_id}",
                data=data,
            )

    def get_description(self, event_id, **data):
        return self.get(f"/events/{event_id}/description/", data=data)

    def get_event_series(self, series_id, **data):
        return self.get(f"/series/{series_id}/")

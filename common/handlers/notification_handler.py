from addons.listing.model.listing import Listing
from addons.notification.model.notification import Notification


class NotificationHandler():

    def __init__(self):
        self.handled_events = ["listing_publish_event","listing_unlock_event"]

    def handle(self,event):
        if event.type not in self.handled_events:
            return
        if event.type == "listing_publish_event":
            self._handle_listing_publish_event(event)
        elif event.type == "listing_unlock_event":
            self._handle_listing_unlock_event(event)


    def _handle_listing_publish_event(self, event):
        textbook_id = event.listing_ins.textbook_id
        query = Listing.select(Listing.owner_id).where((Listing.type=="buyer_post") & (Listing.textbook_id == textbook_id))
        if query.exists():
            import datetime
            data = [
                {"listing_id": event.listing_ins.id,
                 "owner_id": e.owner_id,
                 "is_read":"false",
                 "type": "listing_publish_event",
                 "date_added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                 }
                for e in query
            ]

            for i in range(0, len(data), 100):
                Notification.insert_many(data[i:i + 100]).execute()

    def _handle_listing_unlock_event(self,event):
        listing_id = event.listing_ins.id
        query = Listing.select().where(Listing.id == listing_id)
        if query.exists():
            Notification.add(
                {
                    "listing_id":event.listing_ins.id,
                    "owner_id":event.listing_ins.owner_id,
                    "type": "listing_unlock_event"
                }
            )




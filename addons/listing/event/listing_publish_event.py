

class ListingPublishEvent():

    def __init__(self, listing_ins):
        self.type = "listing_publish_event"
        self.listing_ins = listing_ins

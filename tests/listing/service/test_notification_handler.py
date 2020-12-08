# python3 -m unittest test_notificationHandler.py to run the automated test

import unittest
from addons.user.model.user import User
from common.handlers.notification_handler import NotificationHandler
from utils.MD5_helper import MD5Helper
from addons.listing.model.listing import Listing
from addons.listing.event import listing_publish_event, listing_unlock_event
from addons.notification.model.notification import Notification


class TestNotificationHandler(unittest.TestCase):

    def setUp(self):
        # Prepare dummy data
        self.seller_id = User.insert(
            email='bm2515@nyu.edu',
            password=MD5Helper.hash('12345678')
        ).execute()

        self.buyer_id = User.insert(
            email='yz3919@nyu.edu',
            password=MD5Helper.hash('12345678')
        ).execute()

        self.seller_listing_id = Listing.insert(
            textbook_id=1,
            owner_id=self.seller_id,
            purchase_option="Buy",
            offered_price=100,
            condition="Poor",
            type="seller_post",
            is_published="true"
        ).execute()

        self.buyer_listing_id = Listing.insert(
            textbook_id=1,
            owner_id=self.buyer_id,
            purchase_option="Buy",
            offered_price=100,
            type="buyer_post",
            is_published="true"
        ).execute()

    def tearDown(self):
        # Clean up the test_db
        Listing.delete().execute()
        User.delete().execute()


    def test__handle_listing_publish_event(self):
        listing_ins = Listing.select().where(Listing.id == self.seller_listing_id).get()
        event = listing_publish_event.ListingPublishEvent(
            listing_ins=listing_ins
        )
        NotificationHandler()._handle_listing_publish_event(event)
        query = Notification.select()
        res = [_ for _ in query]

        # The buyer should be getting a notification
        self.assertEqual(1,len(res))
        self.assertEqual(self.buyer_id, res[0].owner_id)

        # Restore the table
        Notification.delete().execute()

    def test__handle_listing_unlock_event(self):

        listing_ins = Listing.select().where(Listing.id == self.seller_listing_id).get()
        event = listing_unlock_event.ListingUnlockEvent(
            listing_ins=listing_ins
        )

        NotificationHandler()._handle_listing_unlock_event(event)
        query = Notification.select()
        res = [_ for _ in query]

        # The seller should be getting a notification
        self.assertEqual(1, len(res))
        self.assertEqual(self.seller_id, res[0].owner_id)

        # Restore the table
        Notification.delete().execute()




if __name__ == '__main__':
    unittest.main()
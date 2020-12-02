#python3 -m unittest test_notificationHandler.py to run the automated test

import unittest
import datetime
import peewee
from addons.user.model.user import User
from utils.MD5_helper import MD5Helper
from TEXbook.addons.listing.model.listing import Listing
from addons.profile.models.profile import Profile
from common.service.event_manager import EventManager
from addons.listing.event import listing_publish_event, listing_unlock_event


class TestNotificationHandler(unittest.TestCase):

    #setUpClass method is run before once before all the test cases in one class are executed
    #tearDownClass method is run onece after all the test cases in one class are executed

    @classmethod
    def setUpClass(cls):
        
        #Create a user
        user_id = cls.create_user()

        #Create a profile
        cls.create_profile(user_id)

        #Create a buyer post
        global buyer_listing_id = cls.create_buyer_post(user_id)

        #Create a seller post
        global seller_listing_id = cls.create_seller_post(user_id)

        global event_manager = EventManager()

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def create_user(cls):

        #Create a user

        email = 'bm2515@nyu.edu'
        password = '12345678'
        user_id = User.insert(
            email=email,
            password=MD5Helper.hash(password)
        ).execute()

        return user_id

    @classmethod
    def create_profile(cls, user_id):

        first_name = "Bilal"
        last_name = "Munawar"
        major = "Computer Science"
        class_year = "2021"
        contact_info = 'WeChat: bilalmunawar'
        avatar_id = 'NULL'

        Profile.insert(
            user_id = user_id,
            first_name = first_name,
            last_name = last_name,
            major = major,
            class_year = class_year,
            contact_info = contact_info,
            avatar_id = avatar_id
        ).execute()


    @classmethod
    def create_seller_post(cls, user_id):

        #Create a seller post listing

        data = cls.get_listing_test_data(user_id, "seller_post")

        seller_listing_id = Listing.insert(
            textbook_id = data["textbook_id"],
            owner_id = data["owner_id"],
            purchase_option = data["purchase_option"],
            offered_price = data["offered_price"],
            condition = data["condition"],
            defect = data["defect"],
            book_image_ids = data["book_image_ids"],
            date_added = data["date_added"],
            type = data["type"],
            is_published = data["is_published"]
        ).execute()

        return seller_listing_id

    @classmethod
    def create_buyer_post(cls, user_id):

        data = cls.get_listing_test_data(user_id, "buyer_post")

        buyer_listing_id = Listing.insert(
            textbook_id = data["textbook_id"],
            owner_id = data["owner_id"],
            purchase_option = data["purchase_option"],
            offered_price = data["offered_price"],
            date_added = data["date_added"],
            type = data["type"],
            is_published = data["is_published"]
        ).execute()

        return buyer_listing_id


    @classmethod
    def get_listing_test_data(cls, user_id, type):

        data = {
        "textbook_id": 1,
        "owner_id" : user_id,
        "purchase_option" : "Buy",
        "offered_price" : 100,
        "condition" : "Poor",
        "defect" : "Stained pages",
        "book_image_ids" : "NULL",
        "date_added" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type" : type,
        "is_published": True
        }

        return data
    
    def test_listing_publish_event(self):

        event = listing_publish_event.ListingPublishEvent(
            listing_ins=seller_listing_id
        )


        event_manager.publish(event)


    def test_listing_unlock_event(self):

        event = listing_unlock_event.ListingUnlockEvent(
            listing_ins=seller_listing_id
        )


        event_manager.publish(event)



if __name__ == '__main__':
    unittest.main()
from base import base_service
from addons.listing.model.listing import Listing
from addons.user.model.user import User
from addons.textbook.model.textbook import Textbook
from addons.listing.service.listingPublishingEvent import execute_event


def get_user_by_id(data):
        users = Listing.select().where((Listing.type == "buyer_post") & (Listing.textbook_id == data["textbook_id"]))
        user_ids = []
        user_emails = []

        for user in users:
            user_ids.append(user.owner_id)

        user_ids = set(user_ids)

        for user_id in user_ids:
            user_email = User.select().where(User.id == user_id).get().email
            user_emails.append(user_email)

        

        return user_emails
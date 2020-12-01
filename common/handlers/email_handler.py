from common.service.email_service import EmailHelper
from addons.listing.model.listing import Listing


class EmailHandler():

    def __init__(self):
        self.handled_events = ["listing_publish_event"]

    def handle(self,event):
        if event.type not in self.handled_events:
            return

        textbook_id = event.listing_ins.textbook_id
        query = Listing.select().where((Listing.textbook_id == textbook_id) & (Listing.type == "buyer_post"))
        if query.exists():
            target_users = []
            for e in query:
                if  e.owner.email_notification_type is None or "send_on_requested_book_published" in e.owner.email_notification_type.split(","):
                    target_users.append(e.owner)

            if len(target_users) > 0:
                from addons.profile.models.profile import Profile
                email_helper = EmailHelper("")
                for user in target_users:
                    profile_ins = Profile.select().where(Profile.user_id == user.id).get()
                    email_content = 'Dear {}, Your requested textbook {} is now available! Click here to check it out.'.format(profile_ins.first_name+' '+profile_ins.last_name , event.listing_ins.textbook.title)
                    email_helper.receiver = user.email
                    email_helper.send_email(subject="Your Requested Textbook is now available", content=email_content)



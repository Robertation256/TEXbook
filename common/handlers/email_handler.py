from addons.listing.model.listing import Listing


class EmailHandler():

    def __init__(self):
        self.handled_events = ["listing_publish_event","listing_unlock_event"]

    def handle(self,event):

        if event.type == "listing_publish_event":
            self._handle_listing_publish(event)

        elif event.type == "listing_unlock_event":
            self._handle_listing_unlocked(event)




    def _handle_listing_unlocked(self,event):
        if event.listing_ins.owner.send_email_on_listing_unlocked == "true":
            from addons.profile.models.profile import Profile
            profile_ins = Profile.select().where(Profile.user_id == event.listing_ins.owner_id).get()
            email = dict()
            email["address"] = event.listing_ins.owner.email
            email["subject"] = f"A User Has Checked Your Listing on '{event.listing_ins.textbook.title}'"
            if event.listing_ins.type == "seller_post":
                email["content"] = f'Dear {profile_ins.first_name + " " + profile_ins.last_name}, a user has checked your seller listing on {event.listing_ins.textbook.title}! He or she might be reaching out for you through your contact information.'
            else:
                email["content"] = f'Dear {profile_ins.first_name + " " + profile_ins.last_name}, a user has checked your buyer request on {event.listing_ins.textbook.title}! He or she might be reaching out for you through your contact information.'

            from jobs.email_task import EmailTask
            task = EmailTask(data=[email])
            task.schedule()

    def _handle_listing_publish(self, event):
        textbook_id = event.listing_ins.textbook_id
        query = Listing.select().where((Listing.textbook_id == textbook_id) & (Listing.type == "buyer_post"))
        if query.exists():
            target_users = []
            for e in query:
                if e.owner.send_email_on_requested_book_available == "true":
                    target_users.append(e.owner)

            if len(target_users) > 0:
                all_emails = []
                from addons.profile.models.profile import Profile
                for user in target_users:
                    profile_ins = Profile.select().where(Profile.user_id == user.id).get()
                    email = dict()
                    email["address"] = user.email
                    email["subject"] = "Your Requested Textbook is now available"
                    email[
                        "content"] = 'Dear {}, Your requested textbook {} is now available! Click here to check it out.'.format(
                        profile_ins.first_name + ' ' + profile_ins.last_name, event.listing_ins.textbook.title)
                    all_emails.append(email)

                from jobs.email_task import EmailTask
                task = EmailTask(data=all_emails)
                task.schedule()


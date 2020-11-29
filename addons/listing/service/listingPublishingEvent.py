import addons.listing.service.event as event
from utils.session import Session
from addons.auth.service.auth_service import AuthService
from addons.profile.models.profile import Profile

class ListingPublishingEvent(object):

    """
    This event class notifies all users who have requested a certain book : Buyer Post
    """

    event_notify = event.Event('send email notifications')
    

def handle_send_notification(sender, event_arg=None):
    
    #parameter: evt_args = [user_emails, title, first_names]
    
    for i in range(len(event_arg[0])):
    #for user_email in event_arg[0]:

        session = Session()
        email = event_arg[0][i]
        title = event_arg[1]
        first_name = event_arg[2][i] 

        email_content = AuthService.send_listing_notification(
            email=email,
            session=session,
            title=title,
            first_name=first_name
        )
        print("email sent:", email_content)


def execute_event(data):
    listing_pub = ListingPublishingEvent()

    #Add handle_send_notification as an event handler
    listing_pub.event_notify += handle_send_notification

    #Call the event handler
    
    listing_pub.event_notify(data)




import event
from utils.session import Session
from addons.auth.service.auth_service import AuthService

class ListingPublishingEvent(object):
    #follow class name convention

    """
    This event class notifies all users who have requested a certain book : Buyer Post

    
    """

    event_notify = event.Event('send email notifications')
    


def handle_send_notification(sender, event_arg=None):
    #Insert the email service to notify all users on their @'nyu' address
    #parameter: evt_args is a python list of all the buyer_post data including students' email
    
    for student_buyer_post in event_arg:

        session = Session()
        email = student_buyer_post

        email_content = AuthService.send_listing_notification(
            email=email,
            session=session
        )
        print("email sent:", email_content)



    
if __name__ == '__main__':

    #Encapsulate the following in a function
    #The correct user list ensures the email is sent to relevant students
    #Call this function everytime a book is published as listing

    listing_pub = ListingPublishingEvent()

    #Add handle_send_notification as an event handler
    listing_pub.event_notify += handle_send_notification

    #Call the event handler
    user_list = ['bm2515@nyu.edu']
    listing_pub.event_notify(user_list)


#In progress: 

# 1) What events are triggered when a listing is published
# 2) How does an email service sends an email to @nyu address



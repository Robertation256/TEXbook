from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template,request
from addons.notifications.model.notification import Notification
from addons.notifications.service import notification_service
from addons.profile.models.profile import Profile

class NotificationResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "notification"
        self.service = notification_service.NotificationService

    def get_notification_message(self, notification_type, title, first_name):
        message=''
        if notification_type == 'publish_listing':
            message = 'Dear {}, your requested listing {} is now available on the website. Click here to check it out!'.format(first_name, title)
        
        elif notification_type == 'seller_post':
            #count of people
            message = 'Dear {}, Your seller information of listing {} was recently unlocked'.format(first_name, title)

        elif notification_type == 'buyer_post':
            message = 'Dear {}, Your buyer post information of listing {} was recently unlocked'.format(first_name, title)

        return message

    @login_required
    def get_notification_list(self):
        #a query search to get all the notification (put max limit) where user_id == owner_id
        pass

    
    def post_notification(self, notification_type, title, first_name):
        user_id = Profile.select().where(Profile.first_name == first_name).get().user_id
        message = self.get_notification_message(notification_type, title, first_name)
        _type = "alert"
        data = {"user_id": user_id, 'message': message, "type" :_type}
        return self.service.add(user_id=user_id, data=data)
        



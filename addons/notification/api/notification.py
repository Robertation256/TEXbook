from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import request,jsonify
from addons.notification.service import notification_service


class NotificationResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "notification"
        self.service = notification_service.NotificationService

    @login_required
    def get_get(self):
        '''
        return all notification a user received
        :return: json
        '''
        user_id = self.service.get_user_id()
        notifications = self.service.get_notifications_by_user_id(user_id)

        return jsonify(notifications)

    @login_required
    def get_is_read(self):
        '''
        set a notification to is_read = True
        :return: dict
        '''
        notification_id = request.args.get("id")
        status = request.args.get("status")
        user_id = self.service.get_user_id()
        res = self.service.set_notification_is_read_by_id(notification_id, user_id,status=status)
        return res

    @login_required
    def get_notification_delete(self):
        '''
        delete a notification
        :return: dict
        '''
        notification_id = request.args.get("id")
        user_id = self.service.get_user_id()
        res = self.service.delete_notification_by_id(notification_id,user_id)
        return res
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
        user_id = self.service.get_user_id()
        notifications = self.service.get_notifications_by_user_id(user_id)
        data = []
        for e in notifications:
            record = {
                "id": e.id,
                "book_title":e.listing.textbook.title,
                "type":e.type,
                "date_added": e.date_added,
                "is_read":e.is_read,
                "listing_type":e.listing.type
            }
            data.append(record)

        return jsonify(data)

    @login_required
    def get_is_read(self):
        notification_id = request.args.get("id")
        status = request.args.get("status")
        user_id = self.service.get_user_id()
        res = self.service.set_notification_is_read_by_id(notification_id, user_id,status=status)
        return res

    @login_required
    def get_notification_delete(self):
        notification_id = request.args.get("id")
        user_id = self.service.get_user_id()
        res = self.service.delete_notification_by_id(notification_id,user_id)
        return res
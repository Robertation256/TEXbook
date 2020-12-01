from base.base_resource import BaseResource
from utils.decorators import login_required
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
        data = [
            {
                "book_title":e.listing.textbook.title,
                "type":e.type,
                "date_added": e.date_added,
                "is_read":e.is_read
            }
            for e in notifications
        ]
        return data

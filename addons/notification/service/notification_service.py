from base import base_service
from addons.notification.model.notification import Notification

class NotificationService(base_service.BaseService):
    model = Notification

    @classmethod
    def get_notifications_by_user_id(cls, user_id):
        query = cls.model.select().where(cls.model.owner_Id == user_id)
        if query.exists():
            return [_ for _ in query]
        return []
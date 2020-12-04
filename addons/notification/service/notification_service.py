from base import base_service
from addons.notification.model.notification import Notification


class NotificationService(base_service.BaseService):
    model = Notification

    @classmethod
    def get_notifications_by_user_id(cls, user_id):
        query = cls.model.select().where(cls.model.owner_id == user_id)
        if query.exists():
            return [_ for _ in query]
        return []

    @classmethod
    def delete_notification_by_id(cls, notification_id, user_id):
        query = cls.model.select().where(cls.model.id == notification_id)
        if query.exists() and query.get().owner_id == user_id:
            cls.model.delete().where(cls.model.id == notification_id).execute()
            return {"status": True}
        return {"status": False}

    @classmethod
    def set_notification_is_read_by_id(cls,notification_id, user_id,status):
        query = cls.model.select().where(cls.model.id == notification_id)
        if query.exists() and query.get().owner_id == user_id:
            if status not in  ["read","unread"]:
                return {"status":False}

            is_read = "true" if status=="read" else "false"
            cls.model.update(is_read=is_read).where(cls.model.id == notification_id).execute()
            return {"status": True}
        return {"status": False}
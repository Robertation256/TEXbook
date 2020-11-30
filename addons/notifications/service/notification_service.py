from base import base_service
from addons.notifications.model.notification import Notification

class NotificationService(base_service.BaseService):
    model = Notification

    @classmethod
    def add(cls, user_id, data):
        cls.model.add({
            "user_id": user_id,
            "message": data["message"],
            "type": data["type"]
        })
        return {"status": True, "msg": None}
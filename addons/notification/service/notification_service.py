from base import base_service
from addons.notification.model.notification import Notification


class NotificationService(base_service.BaseService):
    model = Notification

    @classmethod
    def get_notifications_by_user_id(cls, user_id):
        '''
        get all the notification a user has
        :param user_id:
        :return: dict
        '''
        query = cls.model.select().where(cls.model.owner_id == user_id)
        data = []
        if query.exists():
            from addons.listing.model.listing import Listing
            for e in query:
                query = Listing.select().where(Listing.id == e.listing_id)
                if query.exists():
                    listing_ins = query.get()
                    record = {
                        "id": e.id,
                        "book_title": listing_ins.textbook.title,
                        "type": e.type,
                        "date_added": e.date_added,
                        "is_read": e.is_read,
                        "listing_type": listing_ins.type
                    }
                    data.append(record)
                else:
                    cls.model.delete().where(cls.model.id == e.id).execute()

        return data

    @classmethod
    def delete_notification_by_id(cls, notification_id, user_id):
        '''
        delete a notification
        :param notification_id: int
        :param user_id: int
        :return: dict
        '''
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
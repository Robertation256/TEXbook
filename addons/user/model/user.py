import peewee
from base import base_model


class User(base_model.BaseModel):
    email = peewee.CharField(unique=True, max_length=32)
    password = peewee.CharField(max_length=32)
    unlock_chance = peewee.IntegerField(default=5)
    publish_slot = peewee.IntegerField(default=5)
    is_member = peewee.CharField(default="false")
    email_notification = peewee.CharField(default="true")
    email_notification_freq = peewee.CharField(default="never")
    send_email_on_listing_unlocked = peewee.CharField(default="true")
    send_email_on_requested_book_available = peewee.CharField(default="true")

    @classmethod
    def get_user_id_by_email(cls, email:str):
        query = cls.select().where(cls.email==email)
        if query.exists():
            return query.get().id
        return None

    @classmethod
    def dec_unlock_chance(cls, id):
        unlock_chance = cls.select().where(cls.id == id).get().unlock_chance
        if unlock_chance > 0:
            unlock_chance -= 1
            cls.update(unlock_chance=unlock_chance).where(cls.id==id).execute()

        return unlock_chance

    @classmethod
    def recover_unlock_chance(cls):
        cls.update(unlock_chance=5).execute()

    @classmethod
    def check_member_and_unlock_chance(cls,id):
        query = cls.select(cls.is_member,cls.unlock_chance).where(cls.id == id)
        if query.exists():
            ins = query.get()
            return ins.is_member, ins.unlock_chance
        return "false",0

    @classmethod
    def add(cls, dict): 
        cls.update(
            email_notification=dict["email_notification"],
            email_notification_freq=dict["email_notification_freq"],
            send_email_on_listing_unlocked=dict["send_email_on_listing_unlocked"],
            send_email_on_requested_book_available = dict["send_email_on_requested_book_available"]
        ).where(cls.email == dict["email"]
        ).execute()
        return {"status":True, "message":"Updated Successfully"}

    @classmethod
    def delete_account(cls, email):
        user = cls.get(cls.email == email)
        user.delete_instance()




import peewee
from base import base_model


class User(base_model.BaseModel):
    email = peewee.CharField(unique=True, max_length=32)
    password = peewee.CharField(max_length=32)
    unlock_chance = peewee.IntegerField(default=5)
    is_member = peewee.CharField(default="false")
    email_notification_freq = peewee.CharField(default="never")
    email_notification_type = peewee.CharField(max_length=50)

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




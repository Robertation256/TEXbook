import peewee
from base import base_model


class User(base_model.BaseModel):
    email = peewee.CharField(unique=True, max_length=32)
    password = peewee.CharField(max_length=32)

    @classmethod
    def get_user_id_by_email(cls, email:str):
        query = cls.select().where(cls.email==email)
        if query.exists():
            return query.get().id
        return None


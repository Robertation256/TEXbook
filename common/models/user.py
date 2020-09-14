import peewee
from base import base_model


class User(base_model.BaseModel):
    email = peewee.CharField(unique=True, max_length=32)
    password = peewee.CharField(max_length=32)


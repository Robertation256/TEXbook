import peewee
from base import base_model
from common.models.user import User


class Profile(base_model.BaseModel):
    username = peewee.CharField(max_length=32)
    avatar = peewee.BlobField()
    bio = peewee.CharField(max_length=32)
    user = peewee.ForeignKeyField(model=User, null=False)

import peewee
from base import base_model
from common.models.image import Image
from common.models.user import User


class Profile(base_model.BaseModel):
    username = peewee.CharField(max_length=32)
    avatar = peewee.ForeignKeyField(model=Image, null=True)
    text = peewee.CharField(max_length=32, null=True)
    user = peewee.ForeignKeyField(model=User, null=False)

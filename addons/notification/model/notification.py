import peewee
import datetime
from base import base_model
from addons.user.model.user import User
from addons.listing.model.listing import Listing

class Notification(base_model.BaseModel):
    listing_id = peewee.IntegerField()
    owner = peewee.ForeignKeyField(model=User)
    date_added = peewee.DateTimeField()
    is_read = peewee.CharField(max_length=10,default="false")
    type = peewee.CharField(max_length=30)


    @classmethod
    def add(cls, data:dict):
        cls.insert(
            listing_id=data["listing_id"],
            owner_id = data["owner_id"],
            date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            type = data["type"],
        ).execute()

import peewee
import datetime
from base import base_model
from addons.user.model.user import User

class Notification(base_model.BaseModel):
    owner = peewee.ForeignKeyField(model=User)
    date_added = peewee.DateTimeField()
    message = peewee.CharField(max_length=250,default="Here's the dummy ")
    #Status indicates if the notification has been read (most significant byte) and hidden (least significant byte)
    status = peewee.CharField(max_length=2,default="01")
    type = peewee.CharField(max_length=30,default="alert")


    @classmethod
    def add(cls, data:dict):
        cls.insert(
            owner_id = data["user_id"],
            date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message = data["message"],
            status = "01",
            type = data["type"],
        ).execute()

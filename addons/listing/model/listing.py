import peewee
import datetime
from base import base_model
from addons.user.model.user import User
from addons.textbook.model.textbook import Textbook


class Listing(base_model.BaseModel):
    textbook = peewee.ForeignKeyField(model=Textbook)
    owner = peewee.ForeignKeyField(model=User)
    purchase_option = peewee.CharField()
    offered_price = peewee.DecimalField()
    condition = peewee.CharField(null=True)
    defect = peewee.CharField(null=True)
    book_image_ids = peewee.CharField(null=True)
    date_added = peewee.DateTimeField()
    unlocked_user_ids = peewee.TextField(default="")
    type = peewee.CharField(max_length=30,default="seller_post")


    @classmethod
    def add(cls, data:dict):
        cls.insert(
            textbook_id = data["textbook_id"],
            owner_id = data["user_id"],
            purchase_option = data["purchase_option"],
            offered_price = data["offered_price"],
            condition = data.get("condition"),
            defect = data.get("defect"),
            book_image_ids = data.get("book_image_ids"),
            date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            type=data["type"]
        ).execute()

    @classmethod
    def get_unlocked_user_ids(cls,id):
        query = cls.select(cls.unlocked_user_ids).where(cls.id==id)
        if query.exists():
            res = query.get()
            return res.unlocked_user_ids.split(",")
        return []


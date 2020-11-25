import peewee
import datetime
from base import base_model
from common.models.user import User
from addons.textbook.model.textbook import Textbook


class Listing(base_model.BaseModel):
    textbook = peewee.ForeignKeyField(model=Textbook)
    seller = peewee.ForeignKeyField(model=User)
    purchase_option = peewee.CharField()
    offered_price = peewee.DecimalField()
    condition = peewee.CharField()
    defect = peewee.CharField(null=True)
    book_image_ids = peewee.CharField()
    date_added = peewee.DateTimeField()
    unlocked_user_ids = peewee.TextField(default="")


    @classmethod
    def add(cls, data:dict):
        cls.insert(
            textbook_id = data["textbook_id"],
            seller_id = data["user_id"],
            purchase_option = data["purchase_option"],
            offered_price = data["offered_price"],
            condition = data["condition"],
            defect = data["defect"],
            book_image_ids = data["book_image_ids"],
            date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ).execute()

    @classmethod
    def get_unlocked_user_ids(cls,id):
        query = cls.select(cls.unlocked_user_ids).where(cls.id==id)
        if query.exists():
            res = query.get()
            return res.unlocked_user_ids.split(",")
        return []


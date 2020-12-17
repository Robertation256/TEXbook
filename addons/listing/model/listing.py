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
    is_published = peewee.CharField(max_length=10, default="true")


    @classmethod
    def add(cls, data:dict):
        '''
        add a listing record to DB
        :param data:
        :return: int
        '''
        id = cls.insert(
            textbook_id = data["textbook_id"],
            owner_id = data["user_id"],
            purchase_option = data["purchase_option"],
            offered_price = data["offered_price"],
            condition = data.get("condition"),
            defect = data.get("defect"),
            book_image_ids = data.get("book_image_ids"),
            date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            type=data["type"],
            is_published=data["is_published"]
        ).execute()
        return id

    @classmethod
    def get_unlocked_user_ids(cls,id):
        '''
        get the ids of corresponding user who have unlocked a listing
        :param id:
        :return: dict
        '''
        query = cls.select(cls.unlocked_user_ids).where(cls.id==id)
        if query.exists():
            item = query.get()
            data = item.unlocked_user_ids.split(",")
            res = []
            for i in data:
                if i != "":
                    res.append(i)
            return res

        return []


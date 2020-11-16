import peewee
from base import base_model
from common.models.image import Image



class Textbook(base_model.BaseModel):
    ISBN = peewee.CharField(null=False)
    title = peewee.CharField(null=False)
    author = peewee.CharField(null=False)
    edition = peewee.CharField(null=False)
    publisher = peewee.CharField(null=False)
    price = peewee.DecimalField(null=True)
    book_format = peewee.CharField(null=True)
    cover_image = peewee.ForeignKeyField(model=Image, null=True)

    @classmethod
    def search_by_id(cls, id:int):
        if id is None:
            return None
        res = cls.select().where(cls.id == id)
        if res.exists():
            res = res.get()
            return {
                "ISBN": res.ISBN,
                "title": res.title,
                "author": res.author,
                "edition": res.edition,
                "publisher": res.publisher,
                "price": res.price,
                "book_format": res.book_format,
                "cover_image": res.cover_image
            }
        return None

    @classmethod
    def search_by_keyword(cls, k:str):
        pass
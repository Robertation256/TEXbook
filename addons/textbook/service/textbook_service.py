from base import base_service
from addons.textbook.model.textbook import Textbook


class TextbookService(base_service.BaseService):
    model = Textbook

    @classmethod
    def get_textbook_by_id(cls,id:int):
        query = cls.model.select().where(cls.model.id == id)
        if query.exists():
            res = query.get()
            res.price = round(res.price)
            return res
        return None


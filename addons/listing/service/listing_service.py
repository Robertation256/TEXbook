from base import base_service
from addons.listing.model.listing import Listing


class ListingService(base_service.BaseService):
    model = Listing

    @classmethod
    def add(cls, user_id, data):
        from common.models.image import Image
        img_id_list = Image.add_multiple(data["image_data"])
        img_ids = ",".join([str(i) for i in img_id_list])
        cls.model.add({
            "textbook_id":data["textbook_id"],
            "user_id":user_id,
            "purchase_option": data["purchase_option"],
            "offered_price": data["offered_price"],
            "condition":data["condition"],
            "defect":data["defect"],
            "book_image_ids": img_ids,
        })
        return {"status":True,"msg":None}


    @classmethod
    def get_listing_by_id(cls, id:int):
        query = cls.model.select().where(cls.model.id == id)
        if query.exists():
            return query.get()
        return None

    @classmethod
    def get_listing_by_user_id(cls, user_id: int):
        pass

    @classmethod
    def delete(cls, id: int):
        pass
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
    def get_listing_by_textbook_id(cls, id:int):
        query = cls.model.select().where(cls.model.textbook_id==id)
        if query.exists():
            from addons.profile.models.profile import Profile
            res =  [_ for _ in query]
            for e in res:
                e.offered_price = int(e.offered_price)
                seller_id = e.seller_id
                avatar_id = Profile.get(Profile.user_id==seller_id).avatar_id
                e.avatar_id = avatar_id
            return res

        return []

    @classmethod
    def get_textbook_by_id(cls, id:int):
        from addons.textbook.service.textbook_service import TextbookService
        res = TextbookService.get_textbook_by_id(id)
        return res

    @classmethod
    def get_contact_info_by_id(cls, id:int):
        from common.models.user import User
        user_id = cls.get_user_id()
        user_ins = User.select().where(User.id==user_id).get()
        is_member = user_ins.is_member
        unlock_chance = user_ins.unlock_chance
        if is_member == "false" and unlock_chance <= 0:
            return {"chance_left": 0, "contact_info": None}

        from addons.profile.models.profile import Profile
        listing_owner_id = cls.model.select().where(cls.model.id == id).get().id
        contact_info = Profile.get_contact_info_by_id(listing_owner_id)
        unlock_chance = User.dec_unlock_chance(user_id)
        return {"chance_left":unlock_chance, "contact_info":contact_info}


    @classmethod
    def get_listing_by_user_id(cls, user_id: int):
        pass

    @classmethod
    def delete(cls, id: int):
        pass
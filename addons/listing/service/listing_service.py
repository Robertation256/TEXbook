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

        #A function returns the user credentials (email address) who requested the title = user_list
            #This function runs through all the buyer posts and checks if the textbook_id matches the buyer post

        #A listingPublishingEvent event is triggered with user_list as a parameter

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
        user_id = cls.get_user_id()
        unlocked_user_ids = cls.model.get_unlocked_user_ids(id)
        print(unlocked_user_ids)
        unlock_chance = None
        if str(user_id) not in unlocked_user_ids:
            from common.models.user import User
            is_member, unlock_chance = User.check_member_and_unlock_chance(user_id)
            if is_member == "false" and unlock_chance <= 0:
                return {"chance_left": 0, "contact_info": None}
            else:
                unlock_chance = User.dec_unlock_chance(user_id)
                unlocked_user_ids.append(str(user_id))
                cls.model.update(unlocked_user_ids=",".join(unlocked_user_ids)).where(cls.model.id==id).execute()

        from addons.profile.service.profile_service import ProfileService
        listing_owner_id = cls.model.select().where(cls.model.id == id).get().seller_id
        contact_info = ProfileService.get_contact_info_by_seller_id(listing_owner_id)
        print(contact_info)
        return {"chance_left": unlock_chance, "contact_info":contact_info}


    @classmethod
    def get_listing_by_user_id(cls, user_id: int):
        pass

    @classmethod
    def delete(cls, id: int):
        pass
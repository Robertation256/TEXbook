from base import base_service
from addons.listing.model.listing import Listing
from addons.user.model.user import User
from addons.textbook.model.textbook import Textbook
from addons.listing.service.listingPublishingEvent import execute_event
from addons.listing.service.helper_user import get_user_by_id
from addons.notifications.api.notification import NotificationResource
from addons.profile.models.profile import Profile


class ListingService(base_service.BaseService):
    model = Listing

    @classmethod
    def add(cls, user_id, data):
        if data["type"] == "buyer_post":
            cls.model.add({
                "textbook_id": data["textbook_id"],
                "user_id": user_id,
                "purchase_option": data["purchase_option"],
                "offered_price": data["offered_price"],
                "type": data["type"]
            })
        else:
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
                "type": data["type"]
            })
            
        #----- Begin: Event handlers for notification push ------


        user_email = get_user_by_id(data)
        print('first print')
        print(user_email)
        first_names = []
        for email in user_email:
            user_id = User.select().where(User.email == email).get().id
            
            first_name = Profile.select().where(Profile.user_id == user_id).get().first_name
            first_names.append(first_name)    
        
        
        #Notification on the website
        title = Textbook.select().where(Textbook.id == data["textbook_id"]).get().title

        for i in range(len(first_names)):
            first_name = first_names[i]

            notify = NotificationResource()
            notify.post_notification(notification_type = 'publish_listing', title =title, first_name=first_name)
           
        if data["type"] != "buyer_post":
            #Notification on email

            #Integrate if they have opted for email notification
            title = Textbook.select().where(Textbook.id == data["textbook_id"]).get().title
            user_email = get_user_by_id(data) #python list of email addresses

            print('fellow users requested the title: ')
            print(user_email)
            
            
            data = [user_email, title, first_names]
            # parameter example: data = [[user_email1, user_email2], title]
            execute_event(data)

        #----- End: Event handlers for notification push ------

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
                seller_id = e.owner_id
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
            from addons.user.model.user import User
            is_member, unlock_chance = User.check_member_and_unlock_chance(user_id)
            if is_member == "false" and unlock_chance <= 0:
                return {"chance_left": 0, "contact_info": None}
            else:
                unlock_chance = User.dec_unlock_chance(user_id)
                unlocked_user_ids.append(str(user_id))
                cls.model.update(unlocked_user_ids=",".join(unlocked_user_ids)).where(cls.model.id==id).execute()

        from addons.profile.service.profile_service import ProfileService
        listing_owner_id = cls.model.select().where(cls.model.id == id).get().owner_id
        contact_info = ProfileService.get_contact_info_by_seller_id(listing_owner_id)
        print(contact_info)
        return {"chance_left": unlock_chance, "contact_info":contact_info}


    @classmethod
    def get_listing_by_user_id(cls, user_id: int):
        pass

    @classmethod
    def delete(cls, id: int):
        pass
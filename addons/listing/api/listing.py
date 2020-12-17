from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template,request
from addons.listing.model.listing import Listing
from addons.textbook.model.textbook import Textbook
from addons.listing.service import listing_service
from addons.notification.api.notification import NotificationResource
from addons.profile.models.profile import Profile


class ListingResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "listing"
        self.service = listing_service.ListingService

    @login_required
    def get_listing_publish(self):
        '''
        handles get requests to /listing/listing_publish
        :return: HTML template
        '''
        textbook_options = Textbook.get_title(only_title=False)
        user = self.service.get_user_ins()
        avatar_id = self.service.get_avatar_id()
        return render_template("listing_listing_publish.html",textbook_options=textbook_options,user=user,avatar_id=avatar_id)

    @login_required
    def post_listing_publish(self):
        '''
        handles post requests to /listing/listing_publish
        :return: dict
        '''
        user_email = self.service.get_user_email()
        user_id = self.service.get_user_id()
        image_data = [{
            "user_email": user_email,
            "content": file.read(),
            "type": "seller_upload",
            "image_format":"jpg"
        } for file in request.files.values()]
        f = dict()
        f["textbook_id"] = request.form["textbook_id"]
        f["purchase_option"] = request.form["purchase_option"]
        f["offered_price"] = request.form["offered_price"]
        f["condition"] = request.form["condition"]
        f["defect"] = request.form["defect"]
        f["user_id"] = user_id
        f["image_data"] = image_data
        f["type"] = "seller_post"
        f["is_published"] = "true"
        return self.service.add(user_id=user_id,data=f)

    @login_required
    def get_request_publish(self):
        '''
        handle get request  to /listing/request_publish
        :return: HTML template
        '''
        textbook_options = Textbook.get_title(only_title=False)
        user = self.service.get_user_ins()
        avatar_id = self.service.get_avatar_id()
        return render_template("listing_request_publish.html", textbook_options=textbook_options, user=user,avatar_id=avatar_id)

    @login_required
    def post_request_publish(self):
        '''
        handle post request  to /listing/request_publish
        :return: HTML template
        '''
        user_id = self.service.get_user_id()
        f = dict()
        f["textbook_id"] = request.form["textbook_id"]
        f["purchase_option"] = request.form["purchase_option"]
        f["offered_price"] = request.form["offered_price"]
        f["user_id"] = user_id
        f["type"] = "buyer_post"
        f["is_published"] = "true"
        return self.service.add(user_id=user_id, data=f)

    @login_required
    def get_image_ids(self):

        '''
        handles requests from listing detail pop-ups
        :return: dict
        '''

        listing_id = request.args.get("id")
        listing_ins = Listing.select().where(Listing.id == listing_id).get()
        book_image_ids = listing_ins.textbook.cover_image_id
        res = self.service.get_listing_by_id(listing_id)
        if res is None:
            return {"status":False, "msg":""}

        try:
            #Seller Post
            return {"status": True, "book_image_ids": res.book_image_ids.split(",")}
        except:
            #Buyer Post
            return {"status": True, "book_image_ids": book_image_ids}
           

        #ids = [] if res.book_image_ids is None else res.book_image_ids.split(",")
        #return {"status": True, "book_image_ids": ids}

    @login_required
    def get_view_listing(self):
        '''
        handle get request  to /listing/view_listing
        :return: HTML template
        '''
        #pass a URL variable
        textbook_id = request.args.get("id")
        listing_type = request.args.get("listing_type")
        
        textbook = self.service.get_textbook_by_id(textbook_id)

        #Pass in an argument to return seller of buyer listing post. 
        listings = self.service.get_listing_by_textbook_id(listing_type, textbook_id)
        print(len(listings))

        avatar_id = self.service.get_avatar_id()
        user = self.service.get_user_ins()

        if listing_type == 'buyer_post':
            return render_template("listing_request_view.html",textbook=textbook, listings=listings, avatar_id=avatar_id,user=user)

        elif listing_type == 'seller_post': 
            return render_template("listing_listing_view.html",textbook=textbook, listings=listings, avatar_id=avatar_id,user=user)

    @login_required
    def get_unlock_contact_info(self):
        '''
        handle get request  to /listing/unlock_contact_info
        :return: dict
        '''
        listing_id = request.args.get("id")
        data = self.service.get_contact_info_by_id(listing_id)
        return data

    @login_required
    def get_listing_manage(self):
        '''
        handle get request  to /listing/listing_manage
        :return: HTML template
        '''
        avatar_id = self.service.get_avatar_id()
        user = self.service.get_user_ins()
        published_listing = self.service.get_user_listings(user_id=user.id,type="seller_post",is_published="true")
        posted_request = self.service.get_user_listings(user_id=user.id,type="buyer_post",is_published="true")
        unpublished_listing = self.service.get_user_listings(user_id=user.id,type="seller_post",is_published="false")
        unlocked_listing = self.service.get_user_unlocked_listings(user_id=user.id,type="seller_post")
        unlocked_request = self.service.get_user_unlocked_listings(user_id=user.id,type="buyer_post")
        data = dict()
        data["avatar_id"] = avatar_id
        data["user"] = user
        data["published_listing"] = published_listing
        data["unpublished_listing"] = unpublished_listing
        data["unlocked_listing"] = unlocked_listing
        data["unlocked_request"] = unlocked_request
        data["posted_request"] = posted_request
        print("data:",posted_request)

        return render_template("listing_listing_manage.html", **data)

    @login_required
    def get_lock(self):
        '''
        handle get request  to /listing/lock
        :return: dict
        '''
        listing_id = request.args.get("id")
        user_id = self.service.get_user_id()
        self.service.lock_listing_by_id(listing_id=listing_id,user_id=user_id)
        return {"status":True, "msg":"Succeeds"}

    @login_required
    def get_set(self):
        '''
        handle get request  to /listing/set?id={}&on_shelf={}
        :return: dict
        '''
        user_id = self.service.get_user_id()
        listing_id = request.args.get("id")
        on_shelf = request.args.get("on_shelf")
        if listing_id is None:
            return {"status":False, "msg":"Bad Request"}
        if on_shelf is not None:
            on_shelf = True if on_shelf=="1" else False
            res = self.service.modify_listing(
                listing_id=listing_id,
                data={"on_shelf": on_shelf},
                user_id=user_id
            )
            return res

    @login_required
    def get_delete(self):
        '''
        handle get request  to /listing/delete
        :return: dict
        '''
        listing_id = request.args.get("id")
        user_id = self.service.get_user_id()
        res = self.service.delete_listing_by_id(listing_id=listing_id, user_id=user_id)
        return res

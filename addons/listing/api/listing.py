from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template,request
from addons.textbook.model.textbook import Textbook
from addons.listing.service import listing_service
from addons.notifications.api.notification import NotificationResource
from addons.profile.models.profile import Profile


class ListingResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "listing"
        self.service = listing_service.ListingService

    @login_required
    def get_listing_publish(self):
        textbook_options = Textbook.get_title(only_title=False)
        user = self.service.get_user_ins()
        return render_template("listing_listing_publish.html",textbook_options=textbook_options,user=user)

    @login_required
    def post_listing_publish(self):
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
        textbook_options = Textbook.get_title(only_title=False)
        user = self.service.get_user_ins()
        return render_template("listing_request_publish.html", textbook_options=textbook_options, user=user)

    @login_required
    def post_request_publish(self):
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
        res = self.service.get_listing_by_id(listing_id)
        if res is None:
            return {"status":False, "msg":""}

        return {"status": True, "book_image_ids": res.book_image_ids.split(",")}

    @login_required
    def get_view_listing(self):
        textbook_id = request.args.get("id")
        textbook = self.service.get_textbook_by_id(textbook_id)
        listings = self.service.get_listing_by_textbook_id(textbook_id)
        avatar_id = self.service.get_avatar_id()
        user = self.service.get_user_ins()
        return render_template("listing_view.html",textbook=textbook, listings=listings, avatar_id=avatar_id,user=user)

    @login_required
    def get_unlock_contact_info(self):
        #Push notification to user for unlocked information
        listing_id = request.args.get("id")
        listing = self.service.get_listing_by_id(listing_id)
        title = listing.textbook.title
        notification_type = listing.type
        user = self.service.get_user_ins()
        user_id = user.id
        first_name = Profile.select().where(user_id == user_id).get().first_name

        notify = NotificationResource()
        notify.post_notification(notification_type = notification_type, title =title, first_name=first_name)

        data = self.service.get_contact_info_by_id(listing_id)
        return data

    @login_required
    def get_listing_manage(self):
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
        listing_id = request.args.get("id")
        user_id = self.service.get_user_id()
        self.service.lock_listing_by_id(listing_id=listing_id,user_id=user_id)

    @login_required
    def get_set(self):
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
        listing_id = request.args.get("id")
        user_id = self.service.get_user_id()
        res = self.service.delete_listing_by_id(listing_id=listing_id, user_id=user_id)
        return res


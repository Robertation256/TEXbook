from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template,request
from addons.textbook.model.textbook import Textbook
from addons.listing.service import listing_service


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
        listing_id = request.args.get("id")
        data = self.service.get_contact_info_by_id(listing_id)
        return data
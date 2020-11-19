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
    def get_publish(self):
        textbook_options = Textbook.get_title(only_title=False)
        return render_template("listing_publish.html",textbook_options=textbook_options)

    @login_required
    def post_publish(self):
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
        return self.service.add(user_id=user_id,data=f)

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
        data = {
            "book_image_ids": res.book_image_ids.split(",")
        }
        return {"status": True, "data": data}


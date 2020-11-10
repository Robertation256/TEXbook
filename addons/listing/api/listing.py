from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template


class ListingResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "listing"

    @login_required
    def get_publish(self):
        return render_template("listing_publish.html")

from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template
from addons.home.service.home_service import HomeService

class HomeResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "home"
        self.service = HomeService

    @login_required
    def get(self):
        return render_template("home.html")

    @login_required
    def get_home_resource(self):
        data = self.service.get_search_resource()
        return data



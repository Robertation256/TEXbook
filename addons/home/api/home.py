from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template

class HomeResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "home"

    # @login_required
    def get(self):
        return render_template("home.html")

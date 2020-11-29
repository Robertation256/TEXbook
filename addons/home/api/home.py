from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template, redirect
from addons.home.service.home_service import HomeService

        

class HomeResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "home"
        self.service = HomeService

    @login_required
    def get(self):
        
        #try except block to direct first time users to a profile registration page
        try:
            avatar_id = self.service.get_avatar_id()
            user = self.service.get_user_ins()
            return render_template("home.html",avatar_id=avatar_id,user=user)
        except:
            return redirect("/profile/profile")

        

    @login_required
    def get_home_resource(self):
        data = self.service.get_search_resource()
        return data



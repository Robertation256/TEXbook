from flask import render_template, request
from utils.decorators import login_required
from base.base_resource import BaseResource
from utils.session import Session
from addons.profile.service.profile_service import ProfileService


class ProfileResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "profile"
        self.service = ProfileService

    @login_required
    def get_profile(self):
        session = Session()
        email = session.get("email")
        profile_info = self.service.get_profile_info(email=email)
        user = self.service.get_user_ins()
        return render_template("profile.html", user=user, **profile_info)

    @login_required
    def post_profile(self):
        session = Session()
        email = session.get("email")
        form = dict()
        form["first_name"] = request.form.get("first_name")
        form["last_name"] = request.form.get("last_name")
        form["major"] = request.form.get("major")
        form["class_year"] = request.form.get("class_year")
        form["contact_information"] = request.form.get("contact_information")
        form["avatar_id"] = request.form.get("avatar_id")
        form["email"] = email
        res = self.service.add(data=form)
        return res



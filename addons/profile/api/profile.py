from flask import render_template, request
from utils.decorators import login_required
from base.base_resource import BaseResource
from utils.session import Session
from addons.profile.service.profile_service import ProfileService


class ProfileResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "profile"
        self.profile_service = ProfileService

    @login_required
    def get(self):
        session = Session()
        email = session.get("email")
        profile_info = self.profile_service.get_user_profile(email)
        return render_template("profile.html", **profile_info)

    @login_required
    def post(self):
        session = Session()
        email = session.get("email")
        username = request.form.get("username"),
        grade = request.form.get("grade"),
        contact_info = request.form.get("contact_info"),
        avatar = request.file.get("avatar")
        file_format = self.profile_service.avatar_format_check(avatar.file_name)
        if not file_format:
            return {"status":False, "message": "wrong image format"}
        image_content = avatar.read()
        avatar_id = self.profile_service.add_avatar(
            email=email,
            content=image_content,
            file_format=file_format
        )
        data = {
            "username": username,
            "grade": grade,
            "contact_info": contact_info,
            "avatar_id": avatar_id,
        }
        self.profile_service.update_user_profile(
            email=email,
            data=data
        )



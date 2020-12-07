from flask import render_template, request, redirect
from utils.decorators import login_required
from base.base_resource import BaseResource
from common.service.session import Session
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

    @login_required
    def post_profile_account(self):
        session = Session()
        email = session.get("email")
        password = request.form.get("password")
        from utils.format_checker import password_checker
        password_check = password_checker(password)
        if not password_check:
            return {"status": False, "message": "Bad password format"}

        self.service.update_pwd_by_email(pwd=password, email=email)
        return redirect("/profile/profile")

    @login_required
    def post_profile_notifications(self): 
        session = Session()
        email = session.get("email")
        form = dict() 
        form["email_notification"] = request.form.get("email_notification")
        form["email_notification_freq"] = request.form.get("email_notification_freq")
        form["notificationA"] = request.form.get("user_unlock")
        form["notificationB"] = request.form.get("book_listed")
        email_notification_type = '' 
        if form["notificationA"]: 
            email_notification_type += 'A'
        if form["notificationB"]:
            email_notification_type += 'B'
        form["email_notification_type"] = email_notification_type 
        form["email_notification_type"] = None
        form["email"] = email
        res = self.service.notification_settings(data=form)
        return res

    @login_required
    def post_delete_account(self):
        session = Session()
        email = session.get("email")
        self.service.delete_account(email)
        session["logged_in"] = "false"
        return redirect('/')


    @login_required
    def get_logout(self):
        session = Session()
        session["logged_in"] = "false"
        return redirect("/")

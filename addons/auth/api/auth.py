from base.base_resource import BaseResource
from common.models.user import User
from flask import redirect, render_template, request
from utils.session import Session
from addons.auth.service.auth_service import AuthService


class AuthResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "auth"
        self.service = AuthService

    def get_login(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/home")
        return render_template("auth_login.html")

    def post_login(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/home")

        email = request.form.get("email")
        input_password = request.form.get("password")
        res = self.service.email_pwd_auth(password=input_password, email=email)
        if res["status"]:
            session["logged_in"] = "true"
            session["email"] = email
            session.extend()
            print(f"[LOGIN] Login Succeed: [user_email: {email}]")

        return res


    def get_email_verify(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/home")

        return render_template("auth_email_verify.html")

    def post_email_verify(self):
        session = Session()
        if session.get("login"):
            session.extend()
            return redirect("/home")

        token = request.form.get("token")
        stored_token = session.get("token")
        if stored_token is not None and stored_token == token:
            session["email_verified"] = "true"
            session.expire(900)
            return {"status": True, "message": "Email verify succeeds"}
        else:
            return {"status": False, "message": "Wrong token"}

    def get_register(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/home")
        if session.get("email_verified") != "true":
            return redirect("/auth/email_verify")

        return render_template("auth_register.html")

    def post_register(self):
        session = Session()
        if session.get("logged_in") == " true":
            session.extend()
            return redirect("/home")

        if session.get("email_verified") != "true":
            return redirect("/auth/email_verify")

        password = request.form.get("password")
        email = session.get("email")

        from utils.format_checker import (
            password_checker
        )
        password_check = password_checker(password)
        if not password_check:
            return {"status": False, "message": "Bad password format"}

        self.service.add_user(
            email=email,
            password=password
        )

        print(f"[REGISTER] Register Success. Email: {email}")
        return redirect("/profile/profile")




    def post_token(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/auth/login")

        from utils.format_checker import nyu_email_check
        email = request.form.get("email")
        print("email_received:", email)
        if not nyu_email_check(email):
            return {"status": False, "message": "Email is of wrong format. Please provide NYU email"}

        registered = self.service.is_registered(email=email)
        if request.form.get("reset_password") == "true" and not registered:
            return {"status": False, "message": "This email has not been registered yet. Please register first"}

        if request.form.get("reset_password") != "true" and registered:
            return {"status": False, "message": "This email has been registered"}

        token = self.service.send_token(
            email=email,
            session=session
        )
        print("token sent:", token)
        return {"status": True, "message": "A token has been sent to your mail box"}

    def get_reset_password_email_verify(self):
        session = Session()
        if session.get("logged_in") == " true":
            session.extend()
            return redirect("/home")

        return render_template("auth_reset_password_email_verify.html")

    def post_reset_password_email_verify(self):
        session = Session()
        if session.get("logged_in") == " true":
            session.extend()
            return redirect("/home")
        if session.get("reset_password_email_verified") == "true":
            return redirect("/auth/reset_password")

        token = request.form.get("token")
        stored_token = session.get("token")
        if stored_token is not None and stored_token == token:
            session["reset_password_email_verified"] = "true"
            session.expire(900)
            return {"status": True, "message": "Email verify succeeds"}
        else:
            return {"status": False, "message": "Wrong token"}

    def get_reset_password(self):
        session = Session()
        if session.get("logged_in") == " true":
            session.extend()
            return redirect("/home")
        if session.get("reset_password_email_verified") != "true":
            return redirect("/auth/reset_password_email_verify")

        return render_template("auth_reset_password.html")

    def post_reset_password(self):
        session = Session()
        if session.get("logged_in") == " true":
            session.extend()
            return redirect("/home")
        if session.get("reset_password_email_verified") != "true":
            return redirect("/auth/reset_password_email_verify")

        email = session.get("email")
        password = request.form.get("password")
        from utils.format_checker import password_checker
        password_check = password_checker(password)
        if not password_check:
            return {"status": False, "message": "Bad password format"}

        self.service.update_pwd_by_email(pwd=password,email=email)
        return redirect("/auth/login")

















import logbook
from base.base_resource import BaseResource
from models.user import User
from utils.token_generator import TokenGenerator
from utils.MD5_helper import MD5Helper
from auth.service.email_service import EmailHelper
from flask import redirect, render_template, request
from utils.session import Session


class AuthResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "auth"

    def get_login(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/homepage")
        return render_template("login_page.html")

    def post_login(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/homepage")

        email = request.form.get("email")
        input_password = request.form.get("password")
        query = User.select().where(User.email == email)
        if query.exists():
            stored_password_hash = [ _ for _ in query][0].password
            if MD5Helper.evaluate(input_password, stored_password_hash):
                session["logged_in"] = "true"
                session["email"] = email
                session.extend()
                logbook.info(f"[LOGIN] Login Succeed: [user_email: {email}]")
                print(f"[LOGIN] Login Succeed: [user_email: {email}]")
                return redirect("/homepage")
            else:
                logbook.info("[LOGIN] Login Failed: wrong password.")
                return {"status": False, "message": "wrong password"}
        else:
            logbook.info("[LOGIN] Login Failed: user not found.")
            return {"status": False, "message": "username not found"}


    def get_email_verify(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/homepage")

        return render_template("register_page.html")

    def post_email_verify(self):
        session = Session()
        if session.get("login"):
            session.extend()
            return redirect("/homepage")

        token = request.form.get("token")
        stored_token = session.get("token")
        if stored_token is not None and stored_token == token:
            session["email_verified"] = "true"
            session.expire(900)
            return redirect("/auth/register")
        else:
            return {"status": False, "message": "Wrong token"}

    def get_register(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/homepage")
        if session.get("email_verified") != "true":
            return redirect("/auth/email_verify")

        return render_template("register_page.html")

    def post_register(self):
        session = Session()
        if session.get("logged_in") == " true":
            session.extend()
            return redirect("/homepage")

        if session.get("email_verified") != "true":
            return redirect("/auth/email_verify")

        username = request.form.get("username")
        password = request.form.get("password")
        email = session.get("email")

        from utils.format_checker import (
            password_checker,
            username_checker
        )
        username_check = username_checker(username)
        password_check = password_checker(password)
        if not username_check["status"]:
            return {"status": False, "message": username_check["error"]}
        if not password_check:
            return {"status": False, "message": "Bad password format"}

        from utils.MD5_helper import MD5Helper
        User.insert(
            username=username,
            email=email,
            password=MD5Helper.hash(password)
        ).execute()
        print(f"[REGISTER] Register Success. username: {username}, email: {email}")
        session["logged_in"] = "true"
        session.extend()
        return redirect("/auth/login")


    def post_token(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/auth/login")

        from utils.format_checker import nyu_email_check
        email = request.form.get("email")
        if not nyu_email_check(email):
            logbook.info("[GET EMAIL TOKEN] Wrong email format")
            return {"status": False, "message": "Email is of wrong format. Please provide NYU email"}

        query = User.select().where(User.email == email)
        if query.exists():
            return {"status": False, "message": "This email has been registered"}

        token = TokenGenerator.generate()
        session["token"] = token
        session["email"] = email
        session.expire(600)
        email_helper = EmailHelper(receiver_email=email)
        email_helper.send_token(token)
        return {"status": True, "message": "A token has been sent to your mail box"}













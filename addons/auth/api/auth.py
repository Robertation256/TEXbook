import logbook

from addons.profile.models import Profile
from base.base_resource import BaseResource
from common.models.user import User
from utils.token_generator import TokenGenerator
from utils.MD5_helper import MD5Helper
from addons.auth.service.email_service import EmailHelper
from flask import redirect, render_template, request
from utils.session import Session
import redis


class AuthResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "auth"
        self.conn = redis.Redis('localhost')


    def get_login(self):
        
        #Debugging
        ip_address = request.remote_addr
        response_dict = self.get_redis_response()
        print(response_dict[ip_address])

        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
              #return redirect("/home")
        return render_template("auth_login.html")

    def post_login(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/home")

        #brute force password protection
        ip_address = request.remote_addr
        response_dict = self.get_redis_response()
        
        if ip_address not in response_dict:
            val_attempts = {ip_address:5}
            self.conn.hmset("pythonDict", val_attempts)

        response_dict = self.get_redis_response()
        if int(response_dict[ip_address]) <= 0:
        
            logbook.info("[LOGIN] Login Failed: A maximum of 5 failed login attempts reached. Please re-verify your email address")
            return {"status": False, "message": "All 5 login attempts failed"}
            #Enter your code here
            #redirect to the verification page

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
                return {"status": True, "message": "Login succeeds"}
            else:
                logbook.info("[LOGIN] Login Failed: wrong password.")
                self.modify_login_attempt('dec')
                return {"status": False, "message": "wrong password"}
        else:
            logbook.info("[LOGIN] Login Failed: user not found.")
            self.modify_login_attempt('dec')
            return {"status": False, "message": "Email not found"}


    def get_email_verify(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/homepage")
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
            ip_address = request.remote_addr
            response_dict = self.get_redis_response()
            print('DEBUG')
            print(ip_address in response_dict)
            
            email = session.get('email')

            print(email)
            query = User.select().where(User.email == email)

            print(query.exists())

            if ip_address in response_dict and query.exists():
                self.modify_login_attempt('inc')
                print('at least reached here!')
                return {"status": False, "message": "All 5 login attempts failed-verified"}
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

        from utils.MD5_helper import MD5Helper
        user_id = User.insert(
            email=email,
            password=MD5Helper.hash(password)
        ).execute()
        return redirect("/profile/profile")

        print(f"[REGISTER] Register Success. Email: {email}")

        return redirect("/auth/login")


    def post_token(self):
        session = Session()
        if session.get("logged_in") == "true":
            session.extend()
            return redirect("/auth/login")

        from utils.format_checker import nyu_email_check
        email = request.form.get("email")
        print("email_received:", email)
        if not nyu_email_check(email):
            logbook.info("[GET EMAIL TOKEN] Wrong email format")
            return {"status": False, "message": "Email is of wrong format. Please provide NYU email"}

        query = User.select().where(User.email == email)
        if request.form.get("reset_password") == "true" and not(query.exists()):
            return {"status": False, "message": "This email has not been registered yet. Please register first"}

        if request.form.get("reset_password") != "true" and query.exists():
            ip_address = request.remote_addr
            response_dict = self.get_redis_response()
            if ip_address not in response_dict and query.exists():
                #Add the Robert special case
                return {"status": False, "message": "This email has been registered"}

        token = TokenGenerator.generate()
        session["token"] = token
        session["email"] = email
        session.expire(600)
        email_helper = EmailHelper(receiver_email=email)
        email_helper.send_token(token)
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
        from utils.format_checker import (
            password_checker
        )
        password_check = password_checker(password)
        if not password_check:
            return {"status": False, "message": "Bad password format"}
        hashed_pwd = MD5Helper.hash(password)
        User.update(password=hashed_pwd).where(User.email == email).execute()
        return redirect("/auth/login")


    def get_redis_response(self):

        redis_response = self.conn.hgetall("pythonDict")
        response_dict = {y.decode('ascii'): redis_response.get(y).decode('ascii') for y in redis_response.keys()}

        return response_dict

    #change function file directory (static method: service)
    def modify_login_attempt(self, change='dec'):

        'change: dec, inc'

        ip_address = request.remote_addr
        response_dict = self.get_redis_response()
        if change == 'dec':
            attempts = int(response_dict[ip_address]) - 1
        elif change == 'inc':
            attempts = int(response_dict[ip_address]) + 5
        val_attempts = {ip_address:attempts}
        self.conn.hmset("pythonDict", val_attempts)
        response_dict = self.get_redis_response()
        print(response_dict[ip_address])




    #create a duplicate page with modified js and html













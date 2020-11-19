from base import base_service
from utils.MD5_helper import MD5Helper
from common.models.user import User
from utils.token_generator import TokenGenerator
from addons.auth.service.email_service import EmailHelper



class AuthService(base_service.BaseService):
    model = User


    @classmethod
    def update_pwd_by_email(cls,pwd:str, email:str):
        hashed_pwd = MD5Helper.hash(pwd)
        User.update(password=hashed_pwd).where(User.email == email).execute()

    @classmethod
    def email_pwd_auth(cls,password:str, email:str):
        query = cls.model.select().where(User.email == email)
        if query.exists():
            stored_pwd = query.get().password
            if MD5Helper.evaluate(password, stored_pwd):
                return {"status": True, "message": "Login succeeds"}
            return {"status": False, "message": "wrong password"}

        return {"status": False, "message": "Email not found"}

    @classmethod
    def add_user(cls, email:str, password:str):
        user_id = User.insert(
            email=email,
            password=MD5Helper.hash(password)
        ).execute()

    @classmethod
    def is_registered(cls,email):
        '''
        checks if this email is register or not
        :param email:
        :return: bool
        '''
        query = cls.model.select().where(User.email == email)
        return query.exists()


    @classmethod
    def send_token(cls, email:str, session):
        '''
        send a token to mailbox and update session
        :param email:
        :param session:
        :return:
        '''
        token = TokenGenerator.generate()
        session["token"] = token
        session["email"] = email
        session.expire(600)
        email_helper = EmailHelper(receiver_email=email)
        email_helper.send_token(token)
        return token



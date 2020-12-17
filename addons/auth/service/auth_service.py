from base import base_service
from utils.MD5_helper import MD5Helper
from addons.user.model.user import User
from utils.token_generator import TokenGenerator
from base import base_redis_dict
from common.service.email_service import EmailHelper



class AuthService(base_service.BaseService):
    model = User
    ip_dict = base_redis_dict.BaseRedisDict(name="brute_force_protection")


    @classmethod
    def update_pwd_by_email(cls,pwd:str, email:str):
        '''
        update user password
        :param pwd: user password: String
        :param email: user email: String
        :return: None
        '''
        hashed_pwd = MD5Helper.hash(pwd)
        User.update(password=hashed_pwd).where(User.email == email).execute()

    @classmethod
    def email_pwd_auth(cls,password:str, email:str):
        '''
        authenticate user password
        :param password: user password: String
        :param email: user email: String
        :return: dict
        '''
        query = cls.model.select().where(User.email == email)
        if query.exists():
            stored_pwd = query.get().password
            if MD5Helper.evaluate(password, stored_pwd):
                return {"status": True, "message": "Login succeeds"}

            return {"status": False, "message": "wrong password"}

        return {"status": False, "message": "Email not found"}

    @classmethod
    def add_user(cls, email:str, password:str):
        '''
        add user into database
        :param email: str
        :param password: str
        :return: None
        '''
        User.insert(
            email=email,
            password=MD5Helper.hash(password)
        ).execute()

    @classmethod
    def is_registered(cls,email):
        '''
        checks if this email is register or not
        :param email: str
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
        :return: str
        '''
        token = TokenGenerator.generate()
        session["token"] = token
        session["email"] = email
        session.expire(600)
        email_helper = EmailHelper(receiver_email=email)
        email_helper.send_token(token)
        return token

    @classmethod
    def exceeded_max_attempt(cls,ip):
        '''
        check if an IP exceeds maximum failed attempts
        :param ip: str
        :return: bool
        '''
        chance_left = cls.ip_dict.get(ip)
        if chance_left is None:
            cls.ip_dict[ip] = 5
            return False
        chance_left = int(chance_left)
        if chance_left <= 0:
            cls.ip_dict.extend()
            return True

        return False

    @classmethod
    def dec_login_chance(cls, ip):
        '''
        decrease user login chance by one
        :param ip:
        :return: None
        '''
        chance_left = int(cls.ip_dict.get(ip))
        if chance_left > 0:
            cls.ip_dict[ip] = chance_left-1
        cls.ip_dict.extend()

    @classmethod
    def get_chance_left(cls, ip):
        '''
        get the login chance left for a ip
        :param ip:
        :return: int
        '''
        return int(cls.ip_dict.get(ip))

    @classmethod
    def delete_ip(cls, ip):
        '''
        remove an IP from IP dict
        :param ip:
        :return: None
        '''
        cls.ip_dict.delete(ip)

    @classmethod
    def reset_chances(cls, ip):
        '''
        reset user login chance to 5
        :param ip:
        :return: None
        '''
        cls.ip_dict[ip] = 5

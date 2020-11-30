from base import base_service
from utils.MD5_helper import MD5Helper
from addons.user.model.user import User
from utils.token_generator import TokenGenerator
from base import base_redis_dict
from addons.auth.service.email_service import EmailHelper



class AuthService(base_service.BaseService):
    model = User
    ip_dict = base_redis_dict.BaseRedisDict(name="brute_force_protection")


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

    @classmethod
    def send_listing_notification(cls, email:str, session, title, first_name):
        '''
        send a listing notification to mailbox and update session
        '''
        #email_content = email_template(buyer_post)
        email_content = 'Dear {}, Your requested listing {} is now available! Click here to check it out'.format(first_name, title)
        session["email_content"] = email_content
        session["email"] = email
        session.expire(600)
        email_helper = EmailHelper(receiver_email=email)
        email_helper.send_listing_notification(email_content)
        return email_content

    def email_template(cls, buyer_post):
        email_content = """Dear {}, Your requested title, {} with IBSN: {} at the Date of Publish : {} is now exclusively available 
        on the website! Please feel free to check it out - Insert Listing Link or display""".format(buyer_post['name'], 
        buyer_post['textbook_id'], buyer_post['textbook_ISBN'], buyer_post['DOP'])


    @classmethod
    def exceeded_max_attempt(cls,ip):
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
        chance_left = int(cls.ip_dict.get(ip))
        if chance_left > 0:
            cls.ip_dict[ip] = chance_left-1
        cls.ip_dict.extend()

    @classmethod
    def get_chance_left(cls, ip):
        return int(cls.ip_dict.get(ip))

    @classmethod
    def delete_ip(cls, ip):
        cls.ip_dict.delete(ip)

    @classmethod
    def reset_chances(cls, ip):
        cls.ip_dict[ip] = 5








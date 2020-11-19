from common.models.user import User
from utils.session import Session


class BaseService():
    @classmethod
    def get_user_email(cls):
        session = Session()
        user_email = session.get("email")
        return user_email

    @classmethod
    def get_user_id(cls):
        user_email = cls.get_user_email()
        if user_email is None:
            return None
        return User.get_user_id_by_email(email=user_email)


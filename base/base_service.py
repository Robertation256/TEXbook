from addons.user.model.user import User
from common.service.session import Session


class BaseService():
    @classmethod
    def get_user_email(cls):
        session = Session()
        user_email = session.get("email")
        return user_email

    @classmethod
    def get_user_ins(cls):
        email = cls.get_user_email()
        query = User.select().where(User.email==email)
        if query.exists():
            return query.get()
        return None

    @classmethod
    def get_user_id(cls):
        user_email = cls.get_user_email()
        if user_email is None:
            return None
        return User.get_user_id_by_email(email=user_email)

    @classmethod
    def get_avatar_id(cls):
        user_id = cls.get_user_id()
        if user_id is None:
            return None
        from addons.profile.models.profile import Profile
        return Profile.select().where(Profile.user_id == user_id).get().avatar_id

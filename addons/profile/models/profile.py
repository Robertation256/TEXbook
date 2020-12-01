import peewee
from base import base_model
from addons.image.model.image import Image
from addons.user.model.user import User


class Profile(base_model.BaseModel):
    user = peewee.ForeignKeyField(User, null=False)
    first_name = peewee.CharField(max_length=32)
    last_name = peewee.CharField(max_length=32)
    major = peewee.CharField(max_length=32)
    class_year = peewee.CharField(max_length=32)
    avatar_id = peewee.ForeignKeyField(Image, null=False)
    contact_info = peewee.CharField(max_length=32, null=True)


    @classmethod
    def add(cls, dict):
        user_id = User.select().where(User.email == dict["email"]).get().id
        query = cls.select().where(cls.user_id == user_id)
        if query.exists():
            cls.update(
                first_name=dict["first_name"],
                last_name=dict["last_name"],
                major=dict["major"],
                class_year=dict["class_year"],
                contact_info=dict["contact_information"],
                avatar_id=dict["avatar_id"]
            ).where(
                cls.user_id == user_id
            ).execute()
            return {"status":True, "message":"Update succeeds"}
        else:
            cls.insert(
                user_id = user_id,
                first_name=dict["first_name"],
                last_name=dict["last_name"],
                major=dict["major"],
                class_year=dict["class_year"],
                contact_info=dict["contact_information"],
                avatar_id=dict["avatar_id"]
            ).execute()
            return {"status": True, "message": "Update succeeds"}

    @classmethod
    def get_profile_by_user_id(cls, user_id):
        query = cls.select().where(cls.user_id==user_id)
        if query.exists():
            profile_ins = query.get()
            return profile_ins

    @classmethod
    def get_profile_by_email(cls, user_email:str):
        user = User.select().where(User.email==user_email).get()
        query = cls.select().where(cls.user_id==user.id)
        if query.exists():
            profile_ins = query.get()
            result = {
                "first_name": profile_ins.first_name,
                "last_name": profile_ins.last_name,
                "major": profile_ins.major,
                "class_year": profile_ins.class_year,
                "avatar_id": profile_ins.avatar_id,
                "contact_information": profile_ins.contact_info
            }
            return result
        else:
            return {
                "first_name": "",
                "last_name": "",
                "major": "",
                "class_year": "",
                "avatar_id": 5,
                "contact_info": ""
            }

    @classmethod
    def get_contact_info_by_id(cls, id):
        query = cls.select(cls.first_name,cls.last_name,cls.contact_info).where(cls.id == id)
        if query.exists():
            return query.get()
        return None


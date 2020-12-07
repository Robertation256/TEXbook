from addons.user.model.user import User
from addons.profile.models.profile import Profile
from addons.image.model.image import Image
from utils.MD5_helper import MD5Helper
from base import base_service


class ProfileService(base_service.BaseService):
    model = Profile

    @classmethod
    def add(cls, data:dict):
        res = cls.model.add(data)
        return res

    @classmethod
    def get_profile_info(cls, email:str):
        '''
        get profile data
        :param email:
        :return:
        {
            "first_name":
            "last_name":
            "major":
            "class_year":
            "avatar_id":
            "contact_information":
            "avatar_options":
        }
        '''
        profile_info = cls.model.get_profile_by_email(email)
        avatar_options = Image.get_avatar_ids()
        profile_info["avatar_options"] = avatar_options
        return profile_info

    @classmethod
    def avatar_format_check(cls, file_name: str) -> bool:
        if "." in file_name:
            file_format = file_name.split(".")[-1]
            if file_format in ["jpg","png", "jpeg"]:
                return file_format
        return False

    @classmethod
    def get_contact_info_by_seller_id(cls, id):
        query = cls.model.select(cls.model.last_name,cls.model.first_name,cls.model.contact_info).where(cls.model.user_id==id)
        if query.exists():
            ins = query.get()
            res = dict()
            res["contact_info"] = ins.contact_info
            res["first_name"] = ins.first_name
            res["last_name"] = ins.last_name
            return res
        return None

    @classmethod
    def update_pwd_by_email(cls,pwd:str, email:str):
        hashed_pwd = MD5Helper.hash(pwd)
        User.update(password=hashed_pwd).where(User.email == email).execute()

    @classmethod 
    def notification_settings(cls, data:dict):
        res = User.add(data)
        return res

    @classmethod
    def delete_account(cls, email:str):
        User.delete_account(email)




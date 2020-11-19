from addons.profile.models.profile import Profile
from common.models.image import Image
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


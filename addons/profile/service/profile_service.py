from addons.profile.models.profile import Profile
from common.models.user import User
from common.models.image import Image


class ProfileService(object):
    @classmethod
    def avatar_format_check(cls, file_name: str) -> bool:
        if "." in file_name:
            file_format = file_name.split(".")[-1]
            if file_format in ["jpg","png", "jpeg"]:
                return file_format
        return False

    @classmethod
    def get_user_profile(cls, email: str) -> dict:
        user_ins = User.select().where(User.email==email)
        profile_ins = user_ins.profile
        result = {
            "username": profile_ins.username,
            "grade": profile_ins.grade,
            "contact_info": profile_ins.contact_info,
            "avatar_id": profile_ins.avatar
        }
        return result

    @classmethod
    def add_avatar(cls, email, content, file_format):
        user_id = User.get().where(User.email==email).id
        query = Image.select().where(Image.user_id == user_id & Image.type == "avatar")
        if query.exists():
            image_id = query.get().id
        else:
            image_id = None
        avatar_id = Image.add(
            user_id=user_id,
            content=content,
            type="avatar",
            image_id=image_id,
            image_format=file_format
        )
        return avatar_id


    @classmethod
    def update_user_profile(cls, email:str, data:dict) -> dict:
        print(f"[PROFILE SERVICE] Updating profile [email:{email}, data:{data}]")
        user_ins = User.get().where(User.email == email)
        try:
            Profile.update(
                username=data.get("username"),
                grade=data.get("grade"),
                contact_info=data.get("contact_info"),
                avatar_id=data.get("avatar_id")
            ).where(Profile.id==user_ins.profile_id).execute()
        except:
            return {"status":False, "message": "Profile update failed"}
from base import base_service
from addons.image.model.image import Image


class ImageService(base_service.BaseService):
    model = Image

    @classmethod
    def get_image(cls,image_id,user_email, type):
        if image_id is None:
            return {"status": False, "result": None}
        if user_email is None or user_email == "public":
            query = cls.model.select().where(cls.model.id == image_id)
        else:
            query = cls.model.select().where((cls.model.id == image_id) & (cls.model.owner_email == user_email))

        if query.exists() and type in query.get().type:
            return {"status": True, "result": query.get()}
        else:
            return {"status": False, "result": None}

    @classmethod
    def delete_image_by_ids(cls,image_ids:list):
        if len(image_ids) > 0:
            cls.model.delete().where(cls.model.id << image_ids).execute()

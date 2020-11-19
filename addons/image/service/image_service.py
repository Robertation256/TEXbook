from base import base_service
from common.models.image import Image


class ImageService(base_service.BaseService):
    model = Image

    @classmethod
    def get_image(cls,image_id,user_email, type):
        if image_id is None:
            return {"status": False, "result": None}
        if user_email is None or user_email == "public":
            query = cls.model.select().where((cls.model.id == image_id) & (cls.model.owner_email == "public"))
        else:
            query = cls.model.select().where((cls.model.id == image_id) & (cls.model.owner_email == user_email))

        if query.exists() and type in query.get().type:
            return {"status": True, "result": query.get()}
        else:
            return {"status": False, "result": None}

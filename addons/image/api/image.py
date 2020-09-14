from base.base_resource import BaseResource
from flask import request,Response
from common.models.image import Image
from utils.session import Session


class ImageResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "image"

    def get(self):
        session = Session()
        if session.get("logged_in") != "true":
            return {"status": False, "message": "permission denied"}
        image_id = request.args.get("id")
        if image_id is None:
            return {"status": False, "message": "no image_id"}
        query = Image.select().where(Image.id == image_id)
        if query.exists():
            image_ins = query.get()
            if image_ins.user.email == session.get("email"):
                with open(f"{image_id}.{image_ins.image_format}", "wb") as fp:
                    fp.write(image_ins.content)
                    return Response(fp, mimetype=f"image/{image_ins.image_format}")
            else:
                return {"status": False, "message": "permission denied"}
        else:
            return {"status": False, "message": "image does not exist"}
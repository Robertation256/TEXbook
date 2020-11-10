import io
from base.base_resource import BaseResource
from flask import request, Response, render_template, redirect, send_file
from common.models.image import Image
from utils.session import Session


class ImageResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._prefix = "image"

    def get_page(self):
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

    def get_test(self):
        return render_template("upload_file.html")

    def get_avatar(self):
        image_id = request.args.get("id")
        if image_id is None:
            return {"status": False, "message": "no image_id"}
        result = Image.get_image(image_id,user_email=None, type="avatar")
        if result["status"]:
            image_ins = result["result"]
            return send_file(
                io.BytesIO(image_ins.content),
                mimetype=f"image/{image_ins.image_format}",
                attachment_filename=f'avatar_{image_id}'
            )
        else:
            return result

    def get_resource(self):
        image_id = request.args.get("id")
        if image_id is None:
            return {"status": False, "message": "no image_id"}
        result = Image.get_image(image_id,user_email=None, type="resource")
        if result["status"]:
            image_ins = result["result"]
            return send_file(
                io.BytesIO(image_ins.content),
                mimetype=f"image/{image_ins.image_format}",
                attachment_filename=f'avatar_{image_id}'
            )
        else:
            return result

    def get_bookcover(self):
        image_id = request.args.get("id")
        if image_id is None:
            return {"status": False, "message": "no image_id"}
        result = Image.get_image(image_id,user_email=None, type="bookcover")
        if result["status"]:
            image_ins = result["result"]
            return send_file(
                io.BytesIO(image_ins.content),
                mimetype=f"image/{image_ins.image_format}",
                attachment_filename=f'avatar_{image_id}'
            )
        else:
            return result




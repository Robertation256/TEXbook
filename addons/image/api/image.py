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

    def post_test(self):
        file = request.files.get("image")
        file_format = file.filename.split(".")[-1]

        from common.models.test_image import TestImage
        print("file_content:", file)
        print("image_format:", file_format)
        fp = file.read()
        TestImage.insert(
            content= fp,
            image_format = file_format
        ).execute()
        return render_template("get_file.html")

    def get_test_image(self):
        from common.models.test_image import TestImage
        image_ins = TestImage.select().get()
        image_content = image_ins.content
        image_format = image_ins.image_format
        return send_file(
            io.BytesIO(image_content),
            mimetype="image/jpeg",
            attachment_filename='test'
        )


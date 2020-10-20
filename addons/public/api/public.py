import io
from flask import render_template, redirect, send_file
from base.base_resource import BaseResource
from utils.session import Session


class PublicResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = ""

    def get(self):
        sesson = Session()
        if sesson.get("logged-in") == "true":
            return redirect("/homepage")

        return render_template("index.html")

    def get_image(self):
        with open("cornell-university-82344.jpg", "rb") as fp:
            image_content = fp.read()
        return send_file(
            io.BytesIO(image_content),
            mimetype="image/jpg",
            attachment_filename='test'
        )

    def get_image2(self):
        with open("v2osk-1Z2niiBPg5A-unsplash.jpg", "rb") as fp:
            image_content = fp.read()
        return send_file(
            io.BytesIO(image_content),
            mimetype="image/jpg",
            attachment_filename='test'
        )
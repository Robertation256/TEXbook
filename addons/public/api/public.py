from flask import render_template, redirect
from base.base_resource import BaseResource
from common.service.session import Session


class PublicResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = ""

    def get(self):
        sesson = Session()
        if sesson.get("logged-in") == "true":
            return redirect("/home")

        return render_template("index.html")

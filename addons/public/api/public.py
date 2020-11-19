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

from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template, request
from addons.textbook.model.textbook import Textbook


class TextbookResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "textbook"

    @login_required
    def get_view(self):
        return render_template("textbook_view.html")

    @login_required
    def get_search(self):
        textbook_id =  request.args.get("id")
        res = Textbook.search_by_id(id=textbook_id)
        return res


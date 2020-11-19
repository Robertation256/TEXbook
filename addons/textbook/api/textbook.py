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
        book_name = request.args.get("book_name")
        course_name = request.args.get("course_name")
        subject = request.args.get("subject")
        if textbook_id is not None:
            res = Textbook.search_by_id(id=textbook_id)
            return res

        if book_name is not None:
            res = Textbook.search_by_book_name(book_name)
            return render_template("textbook_view.html",books=res,keyword=book_name)

        if course_name is not None:
            res = Textbook.search_by_course_name(course_name)
            return render_template("textbook_view.html", books=res, keyword=course_name)

        if subject is not None:
            res = Textbook.search_by_subject(subject)
            return render_template("textbook_view.html", books=res, keyword=subject)


    @login_required
    def get_view_listing(self):
        # textbook_id = request.args.get("id")
        return render_template("textbook_view_listing.html")


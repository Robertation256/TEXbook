from base.base_resource import BaseResource
from utils.decorators import login_required
from flask import render_template, request
from addons.textbook.model.textbook import Textbook
from addons.textbook.service import textbook_service

class TextbookResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._prefix = "textbook"
        self.service = textbook_service.TextbookService

    @login_required
    def get_search(self):
        user = self.service.get_user_ins()
        textbook_id =  request.args.get("id")
        book_name = request.args.get("book_name")
        course_name = request.args.get("course_name")
        subject = request.args.get("subject")
        if textbook_id is not None:
            res = Textbook.search_by_id(id=textbook_id)
            return res
        avatar_id = self.service.get_avatar_id()
        if book_name is not None:
            res = Textbook.search_by_book_name(book_name)
            return render_template("textbook_view.html",books=res,keyword=book_name, avatar_id=avatar_id)

        if course_name is not None:
            res = Textbook.search_by_course_name(course_name)
            return render_template("textbook_view.html", books=res, keyword=course_name, avatar_id=avatar_id)

        if subject is not None:
            res = Textbook.search_by_subject(subject)
            return render_template("textbook_view.html", books=res, keyword=subject, avatar_id=avatar_id,user=user)




from base import base_service
from addons.textbook.model.textbook import Textbook
from common.models.course import Course

class HomeService(base_service.BaseService):

    @classmethod
    def get_search_resource(cls):
        title = Textbook.get_title(only_title=True)
        course_name = Course.get_course_name()
        subject = Course.get_subject()
        data = {
            "title": title,
            "course_name": course_name,
            "subject": subject
        }
        return data
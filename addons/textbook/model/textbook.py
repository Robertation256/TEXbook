import peewee
from base import base_model
from addons.image.model.image import Image
from common.models.course import Course




class Textbook(base_model.BaseModel):
    ISBN = peewee.CharField(null=False)
    title = peewee.CharField(null=False)
    author = peewee.CharField(null=False)
    edition = peewee.CharField(null=False)
    publisher = peewee.CharField(null=False)
    price = peewee.DecimalField(null=True)
    book_format = peewee.CharField(null=True)
    cover_image = peewee.ForeignKeyField(model=Image, null=True)

    @classmethod
    def search_by_id(cls, id:int):
        if id is None:
            return None
        res = cls.select().where(cls.id == id)
        if res.exists():
            res = res.get()
            return {
                "ISBN": res.ISBN,
                "title": res.title,
                "author": res.author,
                "edition": res.edition,
                "publisher": res.publisher,
                "price": float(res.price),
                "book_format": res.book_format,
                "cover_image_id": res.cover_image_id
            }
        return None

    @classmethod
    def search_by_book_name(cls, book_name:str):
        query = cls.select().where(cls.title % f"%{book_name}%")
        if query.exists():
            return [_ for _ in query]
        return []

    @classmethod
    def get_title(cls, only_title=False):
        query = cls.select(cls.id, cls.title).distinct()
        if only_title:
            res = [_.title for _ in query]
            return res
        return [_ for _ in query]


    @classmethod
    def search_by_course_name(cls, course_name):
        query = Course.select().where(Course.course_name % f"%{course_name}%")
        if query.exists():
            course_id = query.get().id
            from common.models.textbook_course import Textbook_Course
            query = Textbook_Course.select().where(Textbook_Course.course_id == course_id)
            if query.exists():
                textbook_ids = [_.textbook_id for _ in query]
                res = cls.select().where(cls.id << textbook_ids)
                if res.exists():
                    return [_ for _ in res]
        return []

    @classmethod
    def search_by_subject(cls,subject):
        query = Course.select().where(Course.subject.contains(subject))
        if query.exists():
            course_id = [_.id for _ in query]
            from common.models.textbook_course import Textbook_Course
            query = Textbook_Course.select().where(Textbook_Course.course_id << course_id)
            if query.exists():
                textbook_ids = [_.textbook_id for _ in query]
                res = cls.select().where(cls.id << textbook_ids)
                if res.exists():
                    return [_ for _ in res]
        return []

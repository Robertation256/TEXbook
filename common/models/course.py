import peewee
from base.base_model import BaseModel


class Course(BaseModel):
    course_ID = peewee.CharField(null=False)
    course_name = peewee.CharField(null=False)
    instructor = peewee.CharField(null=False)
    subject = peewee.CharField(null=False)


    @classmethod
    def get_course_name(cls):
        query = cls.select(cls.course_name).distinct()
        res = [_.course_name for _ in query]
        return res

    @classmethod
    def get_subject(cls):
        query = cls.select(cls.subject).distinct()
        res = [_.subject for _ in query]
        return res
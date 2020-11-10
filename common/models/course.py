import peewee
from base.base_model import BaseModel


class Course(BaseModel):
    course_ID = peewee.CharField(null=False)
    course_name = peewee.CharField(null=False)
    instructor = peewee.CharField(null=False)
    subject = peewee.CharField(null=False)
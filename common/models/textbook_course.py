import peewee
from base import base_model
from addons.textbook.model.textbook import Textbook
from common.models.course import Course


class Textbook_Course(base_model.BaseModel):
    textbook = peewee.ForeignKeyField(model=Textbook)
    course = peewee.ForeignKeyField(model=Course)

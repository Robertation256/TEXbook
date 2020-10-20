import peewee
from base import base_model
from common.custom_fields.medium_blob import MediumBlobField


class TestImage(base_model.BaseModel):
    content = MediumBlobField()
    image_format = peewee.CharField()
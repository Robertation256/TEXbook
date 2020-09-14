import peewee
import time
from base import base_model
from common.models.user import User


class Image(base_model.BaseModel):
    content = peewee.BlobField()
    dateAdded = peewee.DateTimeField(null=True)
    user = peewee.ForeignKeyField(model=User)
    type = peewee.CharField(null=True)
    image_format = peewee.CharField()

    @classmethod
    def add(cls,
            user_id: int,
            content,
            type: str,
            image_format: str,
            image_id: int = None,
            ):

        date_time = time.strftime("%Y-%m-%d %H:%M")
        if image_id is None:
            try:
                image_id = cls.insert(
                    user_id=user_id,
                    content=content,
                    dateAdded=date_time,
                    type=type,
                    image_format=image_format
                ).execute()
                return image_id
            except:
                return {"status": False}
        else:
            query = cls.select().where(cls.id==image_id)
            if query.exists():
                cls.update(
                    user_id=user_id,
                    content=content,
                    dateAdded=date_time,
                    image_format=image_format
                ).where(cls.id == image_id).execute()
                return image_id
            else:
                return {"status": False, "message": "image id does not exist."}

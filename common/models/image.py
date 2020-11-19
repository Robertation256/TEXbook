import peewee
import time
from base import base_model
from common.custom_fields.medium_blob import MediumBlobField



class Image(base_model.BaseModel):
    owner_email = peewee.CharField(null=True)
    image_format = peewee.CharField()
    type = peewee.CharField(null=True)
    content = MediumBlobField()
    dateAdded = peewee.DateTimeField(null=True)


    @classmethod
    def add(cls,
            user_email: str,
            content,
            type: str,
            image_format: str,
            image_id: int = None,
            ):

        date_time = time.strftime("%Y-%m-%d %H:%M")
        if image_id is None:    #Perform insertion

            image_id = cls.insert(
                owner_email=user_email,
                content=content,
                dateAdded=date_time,
                type=type,
                image_format=image_format
            ).execute()
            return image_id

            # return {"status": False}
        else:                   #Perform edition
            query = cls.select().where(cls.id==image_id)
            if query.exists():
                cls.update(
                    owner_email=user_email,
                    content=content,
                    dateAdded=date_time,
                    image_format=image_format
                ).where(cls.id == image_id).execute()
                return image_id
            else:
                return {"status": False, "message": "image id does not exist."}


    @classmethod
    def add_multiple(cls, data:list):
        res = []
        for d in data:
            id = cls.add(**d)
            res.append(id)
        return res




    @classmethod
    def get_avatar_ids(
            cls,
    ) -> list:
        query = cls.select().where(cls.type == "avatar")
        return [ _.id for _ in query]
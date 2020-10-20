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
            try:
                image_id = cls.insert(
                    owner_email=user_email,
                    content=content,
                    dateAdded=date_time,
                    type=type,
                    image_format=image_format
                ).execute()
                return image_id
            except:
                return {"status": False}
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
    def get_image(
            cls,
            image_id:int,
            user_email: str
    ):
        print(f"requesting {image_id}")
        if image_id is None:
            return {"status": False, "result": None}
        if user_email is None or user_email == "public":
            query = cls.select().where((cls.id == image_id) & (cls.owner_email == "public"))
        else:
            query = cls.select().where((cls.id == image_id) & (cls.owner_email == user_email))

        if query.exists():
            print(query.get().id)
            return {"status": True, "result": query.get()}
        else:
            return {"status": False, "result": None}

    @classmethod
    def get_avatar_ids(
            cls,
    ) -> list:
        query = cls.select().where(cls.type == "avatar")
        return [ _.id for _ in query]
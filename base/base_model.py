from peewee import Model, MySQLDatabase
from config import user_config

db = MySQLDatabase(
    database=user_config.get("DATABASE"),
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd=""
)
db.connect()


class BaseModel(Model):

    class Meta:
        database = db


from peewee import Model, MySQLDatabase
from config import db_credentials

db = MySQLDatabase(
    database=db_credentials.get("DB_DATABASE"),
    host=db_credentials.get("DB_HOST"),
    port=db_credentials.get("DB_PORT"),
    user = "root"
)

db.connect()


class BaseModel(Model):

    class Meta:
        database = db


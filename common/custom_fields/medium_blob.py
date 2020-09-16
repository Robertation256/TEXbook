from peewee import Field, MySQLDatabase

class MediumBlobField(Field):
    field_type = "mediumblob"
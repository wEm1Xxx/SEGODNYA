from Models.Base import Base
from peewee import *

class Roles(Base):
    id = PrimaryKeyField()
    name = CharField(max_length=30, unique=True)

    class Meta:
        table_name = "roles"
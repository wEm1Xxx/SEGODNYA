from Models.Base import Base
from Models.Users import Users
from peewee import *

class Guests(Base):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, unique=True, backref="guest_profile")
    passport_number = CharField(max_length=50)
    passport_issued_by = CharField(max_length=200, null=True)
    birth_date = DateField(null=True)
    preferences = TextField(null=True)

    class Meta:
        table_name = "guests"
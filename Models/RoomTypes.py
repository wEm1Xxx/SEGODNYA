from Models.Base import Base
from peewee import *

class RoomTypes(Base):
    id = PrimaryKeyField()
    name = CharField(max_length=100)
    description = TextField(null=True)
    base_price = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = "room_types"
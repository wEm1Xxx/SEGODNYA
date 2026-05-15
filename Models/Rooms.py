from Models.Base import Base
from Models.RoomTypes import RoomTypes
from peewee import *

class Rooms(Base):
    id = PrimaryKeyField()
    room_number = CharField(max_length=10, unique=True)
    room_type = ForeignKeyField(RoomTypes, backref="rooms")
    capacity = IntegerField()
    status = CharField(max_length=50, default='available')  # available, occupied, cleaning, maintenance

    class Meta:
        table_name = "rooms"
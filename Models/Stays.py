from Models.Base import Base
from Models.Bookings import Bookings
from Models.Guests import Guests
from Models.Rooms import Rooms
from peewee import *

class Stays(Base):
    id = PrimaryKeyField()
    booking = ForeignKeyField(Bookings, backref="stays")
    guest = ForeignKeyField(Guests, backref="stays")
    room = ForeignKeyField(Rooms, backref="stays")
    check_in_time = DateTimeField(null=True)
    check_out_time = DateTimeField(null=True)
    total_amount = DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        table_name = "stays"
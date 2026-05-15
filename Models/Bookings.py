from Models.Base import Base
from Models.Guests import Guests
from Models.Rooms import Rooms
from peewee import *

class Bookings(Base):
    id = PrimaryKeyField()
    guest = ForeignKeyField(Guests, backref="bookings")
    room = ForeignKeyField(Rooms, backref="bookings")
    check_in_date = DateField()
    check_out_date = DateField()
    status = CharField(max_length=50, default='pending')  # pending, confirmed, checked_in, checked_out, cancelled
    total_price = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(null=True)

    class Meta:
        table_name = "bookings"
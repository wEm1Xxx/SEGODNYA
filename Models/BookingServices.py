from Models.Base import Base
from Models.Bookings import Bookings
from Models.Services import Services
from peewee import *

class BookingServices(Base):
    id = PrimaryKeyField()
    booking = ForeignKeyField(Bookings, backref="services")
    service = ForeignKeyField(Services, backref="bookings")
    quantity = IntegerField(default=1)
    price_at_booking = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = "booking_services"
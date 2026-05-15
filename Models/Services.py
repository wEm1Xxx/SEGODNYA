from Models.Base import Base
from peewee import *

class Services(Base):
    id = PrimaryKeyField()
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    category = CharField(max_length=50)

    class Meta:
        table_name = "services"
from peewee import Model
from Connection.db_connection import connect

class Base(Model):
    class Meta:
        database = connect()
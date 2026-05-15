from Models.Base import Base
from Models.Rooms import Rooms
from Models.Users import Users
from peewee import *

class CleaningTasks(Base):
    id = PrimaryKeyField()
    room = ForeignKeyField(Rooms, backref="cleaning_tasks")
    assigned_to = ForeignKeyField(Users, backref="cleaning_tasks", null=True)
    status = CharField(max_length=50, default='pending')  # pending, in_progress, done
    created_at = DateTimeField(null=True)
    completed_at = DateTimeField(null=True)

    class Meta:
        table_name = "cleaning_tasks"
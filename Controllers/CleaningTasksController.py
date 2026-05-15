from Models.CleaningTasks import CleaningTasks
from datetime import datetime

class CleaningTasksController:
    @classmethod
    def get(cls):
        return CleaningTasks.select()

    @classmethod
    def get_pending(cls):
        return CleaningTasks.select().where(CleaningTasks.status == "pending")

    @classmethod
    def show(cls, id):
        return CleaningTasks.get_or_none(CleaningTasks.id == id)

    @classmethod
    def create(cls, room_id):
        return CleaningTasks.create(
            room_id=room_id,
            status="pending",
            created_at=datetime.now()
        )

    @classmethod
    def complete(cls, id):
        task = CleaningTasks.get_or_none(CleaningTasks.id == id)
        if task and task.status == "pending":
            task.status = "done"
            task.completed_at = datetime.now()
            task.save()
            return task
        return None

    @classmethod
    def assign(cls, id, assigned_to_id):
        task = CleaningTasks.get_or_none(CleaningTasks.id == id)
        if task:
            task.assigned_to_id = assigned_to_id
            task.save()
            return task
        return None
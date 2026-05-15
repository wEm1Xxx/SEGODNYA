from Models.CleaningTasks import CleaningTasks
from Models.Rooms import Rooms
from datetime import datetime

class CleaningController:
    @classmethod
    def get_pending_tasks(cls):
        """Список заданий на уборку."""
        return CleaningTasks.select().where(CleaningTasks.status == "pending")

    @classmethod
    def get_task_by_id(cls, task_id):
        """Задание по id."""
        return CleaningTasks.get_or_none(CleaningTasks.id == task_id)

    @classmethod
    def complete_task(cls, task_id):
        """Завершение задания на уборку."""
        task = CleaningTasks.get_or_none(CleaningTasks.id == task_id)
        if not task:
            return None, "Задание не найдено"

        task.status = "done"
        task.completed_at = datetime.now()
        task.save()

        room = task.room
        room.status = "available"
        room.save()

        return task, "Уборка завершена"
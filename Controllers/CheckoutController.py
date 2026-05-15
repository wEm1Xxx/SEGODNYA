from Models.Stays import Stays
from Models.Rooms import Rooms
from Models.CleaningTasks import CleaningTasks
from datetime import datetime

class CheckoutController:
    @classmethod
    def checkout(cls, stay_id):
        """Выезд гостя."""
        stay = Stays.get_or_none(Stays.id == stay_id)
        if not stay or stay.check_out_time:
            return None, "Проживание не найдено или уже завершено"

        # Обновляем время выезда
        stay.check_out_time = datetime.now()
        stay.save()

        # Обновляем статус бронирования
        booking = stay.booking
        booking.status = "checked_out"
        booking.save()

        # Обновляем статус номера
        room = stay.room
        room.status = "cleaning"
        room.save()

        # Создаём задание на уборку
        CleaningTasks.create(room_id=room.id, status="pending", created_at=datetime.now())

        return stay, "Выезд выполнен успешно"
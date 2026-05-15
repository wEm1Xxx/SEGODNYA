from Models.Bookings import Bookings
from Models.Rooms import Rooms
from Models.Stays import Stays
from datetime import datetime

class CheckinController:
    @classmethod
    def checkin(cls, booking_id, room_id):
        """Заезд гостя."""
        booking = Bookings.get_or_none(Bookings.id == booking_id)
        if not booking or booking.status != "confirmed":
            return None, "Бронирование не найдено или не подтверждено"

        room = Rooms.get_or_none(Rooms.id == room_id)
        if not room or room.status != "available":
            return None, "Номер недоступен"

        # Обновляем статус номера
        room.status = "occupied"
        room.save()

        # Обновляем статус бронирования
        booking.status = "checked_in"
        booking.save()

        # Создаём запись о проживании
        stay = Stays.create(
            booking_id=booking.id,
            guest_id=booking.guest_id,
            room_id=room.id,
            check_in_time=datetime.now(),
            total_amount=booking.total_price
        )

        return stay, "Заезд выполнен успешно"
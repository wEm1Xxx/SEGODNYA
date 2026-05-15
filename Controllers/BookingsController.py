from Models.Bookings import Bookings
from Models.Guests import Guests
from Models.Users import Users
from Models.Stays import Stays
from datetime import datetime


class BookingsController:
    @classmethod
    def get(cls):
        """Все бронирования."""
        return Bookings.select().order_by(Bookings.check_in_date)

    @classmethod
    def show(cls, id):
        """Бронирование по id."""
        return Bookings.get_or_none(Bookings.id == id)

    @classmethod
    def get_by_guest(cls, guest_id):
        """Бронирования гостя."""
        return Bookings.select().where(Bookings.guest_id == guest_id)

    @classmethod
    def search_by_phone(cls, phone):
        """Поиск бронирований по телефону гостя."""
        return (Bookings
                .select()
                .join(Guests)
                .join(Users)
                .where(Users.phone == phone))

    @classmethod
    def is_room_available(cls, room_id, check_in_date, check_out_date):
        """Проверяет, свободен ли номер на указанные даты."""
        overlapping_bookings = Bookings.select().where(
            (Bookings.room_id == room_id) &
            (Bookings.status.in_(['confirmed', 'checked_in'])) &
            (Bookings.check_in_date < check_out_date) &
            (Bookings.check_out_date > check_in_date)
        )

        if overlapping_bookings.count() > 0:
            return False

        overlapping_stays = Stays.select().where(
            (Stays.room_id == room_id) &
            (Stays.check_out_time.is_null(True))
        )

        return overlapping_stays.count() == 0

    @classmethod
    def create(cls, guest_id, room_id, check_in_date, check_out_date, total_price):
        """Создание бронирования."""
        try:
            booking = Bookings.create(
                guest_id=guest_id,
                room_id=room_id,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                total_price=total_price,
                status="confirmed",
                created_at=datetime.now()
            )
            return booking
        except Exception as e:
            print(f"[ERROR] BookingsController.create: {e}")
            return None

    @classmethod
    def update_status(cls, id, status):
        """Обновление статуса бронирования."""
        booking = Bookings.get_or_none(Bookings.id == id)
        if booking:
            booking.status = status
            booking.save()
            return booking
        return None

    @classmethod
    def cancel(cls, id):
        """Отмена бронирования."""
        return cls.update_status(id, "cancelled")
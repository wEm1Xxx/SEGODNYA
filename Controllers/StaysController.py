from Models.Stays import Stays
from datetime import datetime

class StaysController:
    @classmethod
    def get(cls):
        return Stays.select()

    @classmethod
    def get_active(cls):
        return Stays.select().where(Stays.check_out_time.is_null(True))

    @classmethod
    def show(cls, id):
        return Stays.get_or_none(Stays.id == id)

    @classmethod
    def create(cls, booking_id, guest_id, room_id, total_amount):
        return Stays.create(
            booking_id=booking_id,
            guest_id=guest_id,
            room_id=room_id,
            check_in_time=datetime.now(),
            total_amount=total_amount
        )

    @classmethod
    def checkout(cls, id):
        stay = Stays.get_or_none(Stays.id == id)
        if stay and not stay.check_out_time:
            stay.check_out_time = datetime.now()
            stay.save()
            return stay
        return None
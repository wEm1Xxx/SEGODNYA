from Models.Guests import Guests

class GuestsController:
    @classmethod
    def get(cls):
        return Guests.select()

    @classmethod
    def show(cls, id):
        return Guests.get_or_none(Guests.id == id)

    @classmethod
    def show_by_user_id(cls, user_id):
        return Guests.get_or_none(Guests.user_id == user_id)

    @classmethod
    def create(cls, user_id, passport_number="", preferences=""):
        return Guests.create(
            user_id=user_id,
            passport_number=passport_number,
            preferences=preferences
        )

    @classmethod
    def update(cls, id, **fields):
        for key, value in fields.items():
            Guests.update({key: value}).where(Guests.id == id).execute()
from Models.Rooms import Rooms

class RoomsController:
    @classmethod
    def get(cls):
        return Rooms.select()

    @classmethod
    def get_available(cls):
        return Rooms.select().where(Rooms.status == "available")

    @classmethod
    def show(cls, id):
        return Rooms.get_or_none(Rooms.id == id)

    @classmethod
    def show_by_number(cls, room_number):
        return Rooms.get_or_none(Rooms.room_number == room_number)

    @classmethod
    def create(cls, room_number, room_type_id, capacity):
        return Rooms.create(
            room_number=room_number,
            room_type_id=room_type_id,
            capacity=capacity,
            status="available"
        )

    @classmethod
    def update_status(cls, id, status):
        room = Rooms.get_or_none(Rooms.id == id)
        if room:
            room.status = status
            room.save()
            return room
        return None

    @classmethod
    def delete(cls, id):
        Rooms.delete().where(Rooms.id == id).execute()
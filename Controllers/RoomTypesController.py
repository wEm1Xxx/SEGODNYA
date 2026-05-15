from Models.RoomTypes import RoomTypes

class RoomTypesController:
    @classmethod
    def get(cls):
        return RoomTypes.select()

    @classmethod
    def show(cls, id):
        return RoomTypes.get_or_none(RoomTypes.id == id)

    @classmethod
    def create(cls, name, base_price, description=None):
        return RoomTypes.create(
            name=name,
            base_price=base_price,
            description=description
        )
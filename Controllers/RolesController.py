from Models.Roles import Roles

class RolesController:
    @classmethod
    def get(cls):
        return Roles.select()

    @classmethod
    def show(cls, id):
        return Roles.get_or_none(Roles.id == id)

    @classmethod
    def show_by_name(cls, name):
        return Roles.get_or_none(Roles.name == name)
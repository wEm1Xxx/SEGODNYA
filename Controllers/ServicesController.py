from Models.Services import Services

class ServicesController:
    @classmethod
    def get(cls):
        return Services.select()

    @classmethod
    def show(cls, id):
        return Services.get_or_none(Services.id == id)

    @classmethod
    def get_by_category(cls, category):
        return Services.select().where(Services.category == category)

    @classmethod
    def create(cls, name, price, category):
        return Services.create(
            name=name,
            price=price,
            category=category
        )
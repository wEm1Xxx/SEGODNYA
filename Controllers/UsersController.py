from Models.Users import Users
import bcrypt
from datetime import datetime

class UsersController:
    @classmethod
    def get(cls):
        """Все пользователи."""
        return Users.select()

    @classmethod
    def show(cls, id):
        """Пользователь по id или None."""
        return Users.get_or_none(Users.id == id)

    @classmethod
    def show_login(cls, login_value):
        """Пользователь по email или username."""
        user = Users.get_or_none(Users.email == login_value)
        if user is None:
            user = Users.get_or_none(Users.username == login_value)
        return user

    @classmethod
    def add(cls, username, email, password, role_id, **kwargs):
        """Создаёт пользователя с указанной ролью."""
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")
        return Users.create(
            username=username,
            email=email,
            password_hash=password_hash,
            role_id=role_id,
            created_at=datetime.now(),
            **kwargs
        )

    @classmethod
    def auth(cls, login_value, password):
        """Проверка входа: возвращает объект Users или None."""
        user = cls.show_login(login_value)
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return user
        return None

    @classmethod
    def update(cls, id, **fields):
        """Обновление полей пользователя."""
        for key, value in fields.items():
            Users.update({key: value}).where(Users.id == id).execute()

    @classmethod
    def delete(cls, id):
        """Удаление пользователя."""
        Users.delete().where(Users.id == id).execute()
from Models.Base import Base
from Models.Roles import Roles
from peewee import *
import bcrypt
from datetime import datetime

class Users(Base):
    id = PrimaryKeyField()
    username = CharField(max_length=50, unique=True)
    email = CharField(max_length=100, unique=True)
    password_hash = CharField(max_length=255)
    role = ForeignKeyField(Roles, backref="users")
    first_name = CharField(max_length=50, null=True)
    last_name = CharField(max_length=50, null=True)
    phone = CharField(max_length=20, null=True)
    created_at = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)

    class Meta:
        table_name = "users"

    @classmethod
    def create_user(cls, username, email, password, role_id, **kwargs):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return cls.create(
            username=username,
            email=email,
            password_hash=password_hash,
            role_id=role_id,
            **kwargs
        )

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @classmethod
    def find_by_username(cls, username):
        try:
            return cls.get(cls.username == username)
        except:
            return None

    @classmethod
    def find_by_email(cls, email):
        try:
            return cls.get(cls.email == email)
        except:
            return None

    @classmethod
    def find_by_id(cls, uid):
        try:
            return cls.get_by_id(uid)
        except:
            return None

    def get_role_name(self):
        return self.role.name if self.role else "Гость"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.username

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.get_role_name(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone
        }

    # Flask-Login required methods
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
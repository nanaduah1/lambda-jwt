from functools import cached_property

import peewee

from auth.hasher import hasher
from config import initialize_db

db = initialize_db()


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField(max_length=150, unique=True)
    first_name = peewee.CharField(max_length=150)
    last_name = peewee.CharField(max_length=150)
    email = peewee.CharField(max_length=254, null=True)
    last_login = peewee.DateTimeField(null=True)
    password = peewee.CharField(max_length=128)
    is_superuser = peewee.BooleanField(default=False)
    is_active = peewee.BooleanField(default=False)

    class Meta:
        table_name = "auth_user"

    def set_password(self, password):
        self.password = hasher.encode(password)

    @cached_property
    def permissions(self):
        query = self.groups.select(
            Group.name,
        ).tuples()
        return (p[0] for p in query.iterator())


class Group(BaseModel):
    name = peewee.CharField(max_length=150)


class UserGroup(BaseModel):
    group = peewee.ForeignKeyField(Group, backref="users")
    user = peewee.ForeignKeyField(User, backref="groups")

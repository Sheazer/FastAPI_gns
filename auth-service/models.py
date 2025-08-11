from tortoise import fields, models
from passlib.hash import bcrypt

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(64, unique=True)
    password_hash = fields.CharField(128)
    tin = fields.CharField(32, null=True)

    @classmethod
    async def create_user(cls, username: str, password: str, tin: str = None):
        obj = await cls.create(username=username, password_hash=bcrypt.hash(password), tin=tin)
        return obj

    @classmethod
    async def authenticate(cls, username: str, password: str):
        user = await cls.get_or_none(username=username)
        if user and bcrypt.verify(password, user.password_hash):
            return user
        return None

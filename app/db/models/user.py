from tortoise import fields
from tortoise.models import Model


class User(Model):
    name = fields.CharField(max_length=100)
    age = fields.IntField()
    is_active = fields.BooleanField(default=False)

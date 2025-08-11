from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid
from tortoise.fields import JSONField

class ESFDocument(models.Model):
    id = fields.IntField(pk=True)
    document_uuid = fields.CharField(64, default=lambda: str(uuid.uuid4()), unique=True)
    legal_person_tin = fields.CharField(32)
    data = JSONField()
    status = fields.CharField(20, default="draft")
    created_by = fields.IntField(null=True)  # user id from auth service
    created_at = fields.DatetimeField(auto_now_add=True)

ESF_Pydantic = pydantic_model_creator(ESFDocument, name="ESF")

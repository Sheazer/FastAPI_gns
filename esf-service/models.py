from tortoise import fields
from tortoise.models import Model
from uuid import UUID


class PaymentType(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=20, null=True)
    name = fields.CharField(max_length=255, null=True)


class Currency(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=10, null=True)
    name = fields.CharField(max_length=50, null=True)


class Status(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=20, null=True)
    name = fields.CharField(max_length=100, null=True)


class ReceiptType(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=20, null=True)
    name = fields.CharField(max_length=255, null=True)


class DeliveryType(Model):
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=20, null=True)
    name = fields.CharField(max_length=255, null=True)


class LegalPerson(Model):
    id = fields.IntField(pk=True)
    pin = fields.CharField(max_length=20, null=True)
    fullName = fields.CharField(max_length=255, null=True)
    mainFullName = fields.CharField(max_length=255, null=True)
    mainPin = fields.CharField(max_length=20, null=True)


class Contractor(Model):
    id = fields.IntField(pk=True)
    pin = fields.CharField(max_length=20, null=True)
    fullName = fields.CharField(max_length=255, null=True)
    mainFullName = fields.CharField(max_length=255, null=True)
    mainPin = fields.CharField(max_length=20, null=True)


class VatTaxType(Model):
    id = fields.IntField(pk=True)
    rate = fields.DecimalField(max_digits=5, decimal_places=2, null=True)
    name = fields.CharField(max_length=255, null=True)
    code = fields.CharField(max_length=20, null=True)


class Invoice(Model):
    id = fields.IntField(pk=True)
    documentUuid = fields.UUIDField()
    totalAmount = fields.DecimalField(max_digits=15, decimal_places=2)
    createdDate = fields.DateField(null=True)
    deliveryDate = fields.DateField(null=True)
    invoiceDate = fields.DateField(null=True)
    ownedCrmReceiptCode = fields.CharField(max_length=255, null=True)
    invoiceNumber = fields.CharField(max_length=100, null=True)
    number = fields.CharField(max_length=100, null=True)
    note = fields.TextField(null=True)
    correctedReceiptUuid = fields.CharField(max_length=255, null=True)
    isResident = fields.BooleanField(null=True)

    paymentType = fields.ForeignKeyField("models.PaymentType", related_name="invoices", null=True)
    currency = fields.ForeignKeyField("models.Currency", related_name="invoices", null=True)
    status = fields.ForeignKeyField("models.Status", related_name="invoices", null=True)
    receiptType = fields.ForeignKeyField("models.ReceiptType", related_name="invoices", null=True)
    deliveryType = fields.ForeignKeyField("models.DeliveryType", related_name="invoices", null=True)
    legalPerson = fields.ForeignKeyField("models.LegalPerson", related_name="invoices", null=True)
    contractor = fields.ForeignKeyField("models.Contractor", related_name="invoices", null=True)
    vatTaxType = fields.ForeignKeyField("models.VatTaxType", related_name="invoices", null=True)

    class Meta:
        table = "invoices"
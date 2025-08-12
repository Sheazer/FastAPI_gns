from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

# Основная модель для документа
class ESFModel(models.Model):
    """
    Модель Tortoise ORM для документа ЭСФ.
    Использует JSONField для вложенных данных, таких как catalogEntries.
    """
    id = fields.IntField(pk=True)
    document_uuid = fields.CharField(max_length=64, default=None, null=True, unique=True)
    legal_person_tin = fields.CharField(max_length=32)
    status = fields.CharField(max_length=20, default="draft")
    created_by = fields.IntField(null=True) 
    created_at = fields.DatetimeField(auto_now_add=True)

    foreignName = fields.CharField(max_length=255, null=True, description="Наименование иностранца")
    isBranchDataSent = fields.BooleanField(default=False, description="Отправить от имени филиала")
    isPriceWithoutTaxes = fields.BooleanField(default=False, description="Цена без налогов")
    affiliateTin = fields.CharField(max_length=32, null=True, description="ИНН филиала")
    isIndustry = fields.BooleanField(default=False, description="Отраслевые")
    ownedCrmReceiptCode = fields.CharField(max_length=255, null=True, description="Номер учетной системы")
    operationTypeCode = fields.CharField(max_length=255, description="Код вида операции")
    deliveryDate = fields.DateField(description="Дата поставки")
    deliveryTypeCode = fields.CharField(max_length=255, description="Код вида поставки")
    isResident = fields.BooleanField(description="Субъект Кыргызской Республики")
    contractorTin = fields.CharField(max_length=32, description="ИНН покупателя")
    supplierBankAccount = fields.CharField(max_length=255, null=True, description="Номер банковского счета поставщика")
    contractorBankAccount = fields.CharField(max_length=255, null=True, description="Номер банковского счета покупателя")
    currencyCode = fields.CharField(max_length=3, description="Код валюты")
    countryCode = fields.CharField(max_length=3, null=True, description="Код страны")
    currencyRate = fields.DecimalField(max_digits=12, decimal_places=4, null=True, description="Курс валюты к сому")
    totalCurrencyValue = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="Общая стоимость")
    totalCurrencyValueWithoutTaxes = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="Общая стоимость без налогов")
    supplyContractNumber = fields.CharField(max_length=255, null=True, description="Номер договора на поставку")
    contractStartDate = fields.DateField(null=True, description="Дата заключения на поставку")
    comment = fields.TextField(null=True, description="Комментарий")
    deliveryCode = fields.CharField(max_length=255, description="Код поставки")
    paymentCode = fields.CharField(max_length=255, description="Код формы оплаты")
    taxRateVATCode = fields.CharField(max_length=255, description="Код ставки НДС")
 
    # Вложенные поля, хранятся как JSON
    catalogEntries = fields.JSONField(description="Товары", null=True)
    openingBalances = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="Сальдо на начало")
    assessedContributionsAmount = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="Начислено")
    paidAmount = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="Оплачено")
    penaltiesAmount = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="Штраф")
    finesAmount = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="Пеня")
    closingBalances = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="Сальдо на конец")
    amountToBePaid = fields.DecimalField(max_digits=12, decimal_places=2, null=True, description="К оплате")
    personalAccountNumber = fields.CharField(max_length=255, null=True, description="Лицевой счет")

# Pydantic-модель для валидации и сериализации
ESF_Pydantic = pydantic_model_creator(ESFModel, name="ESF")


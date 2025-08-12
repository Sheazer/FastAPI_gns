from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import date

# --- Определяем модели данных с помощью Pydantic ---

class CatalogEntry(BaseModel):
    """
    Модель для товарной позиции в каталоге.
    """
    id: int
    unitClassificationCode: str
    salesTaxCode: str
    customsAuthorityCode: Optional[str] = None
    quantity: Decimal
    price: Decimal
    vatAmount: Optional[Decimal] = None
    salesTaxAmount: Optional[Decimal] = None
    amountWithoutTaxes: Optional[Decimal] = None
    totalAmount: Optional[Decimal] = None

class InvoiceData(BaseModel):
    """
    Основная модель данных, которая будет приниматься эндпоинтом.
    Все поля соответствуют вашему описанию.
    """
    # Обязательные поля
    isBranchDataSent: bool
    isPriceWithoutTaxes: bool
    operationTypeCode: str
    deliveryDate: date
    deliveryTypeCode: str
    isResident: bool
    contractorTin: str
    currencyCode: str
    deliveryCode: str
    paymentCode: str
    taxRateVATCode: str
    catalogEntries: List[CatalogEntry]

    # Необязательные поля (Optional)
    foreignName: Optional[str] = None
    affiliateTin: Optional[str] = None
    isIndustry: Optional[bool] = None
    ownedCrmReceiptCode: Optional[str] = None
    supplierBankAccount: Optional[str] = None
    contractorBankAccount: Optional[str] = None
    countryCode: Optional[str] = None
    currencyRate: Optional[Decimal] = None
    totalCurrencyValue: Optional[Decimal] = None
    totalCurrencyValueWithoutTaxes: Optional[Decimal] = None
    supplyContractNumber: Optional[str] = None
    contractStartDate: Optional[date] = None
    comment: Optional[str] = None
    openingBalances: Optional[Decimal] = None
    assessedContributionsAmount: Optional[Decimal] = None
    paidAmount: Optional[Decimal] = None
    penaltiesAmount: Optional[Decimal] = None
    finesAmount: Optional[Decimal] = None
    closingBalances: Optional[Decimal] = None
    amountToBePaid: Optional[Decimal] = None
    personalAccountNumber: Optional[str] = None

class ApiResponse(BaseModel):
    """
    Модель для ответа сервера.
    """
    responseId: str
    documentUuid: str





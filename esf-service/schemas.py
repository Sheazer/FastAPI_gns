from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class CatalogEntry(BaseModel):
    product_id: str
    quantity: float
    price: float

class ESFCreate(BaseModel):
    legal_person_tin: str
    foreignName: Optional[str] = None
    isBranchDataSent: bool = False
    isPriceWithoutTaxes: bool = False
    affiliateTin: Optional[str] = None
    isIndustry: bool = False
    ownedCrmReceiptCode: Optional[str] = None
    operationTypeCode: str
    deliveryDate: date
    deliveryTypeCode: str
    isResident: bool
    contractorTin: str
    supplierBankAccount: Optional[str] = None
    contractorBankAccount: Optional[str] = None
    currencyCode: str
    countryCode: Optional[str] = None
    currencyRate: Optional[float] = None
    totalCurrencyValue: Optional[float] = None
    totalCurrencyValueWithoutTaxes: Optional[float] = None
    supplyContractNumber: Optional[str] = None
    contractStartDate: Optional[date] = None
    comment: Optional[str] = None
    deliveryCode: str
    paymentCode: str
    taxRateVATCode: str
    catalogEntries: List[CatalogEntry]
    openingBalances: Optional[Dict[str, Any]] = None
    assessedContributionsAmount: Optional[float] = None
    paidAmount: Optional[float] = None
    penaltiesAmount: Optional[float] = None
    finesAmount: Optional[float] = None
    closingBalances: Optional[float] = None
    amountToBePaid: Optional[float] = None
    personalAccountNumber: Optional[str] = None

    # @validator("currencyCode")
    # def validate_currency_code(cls, v):
    #     if len(v) != 3:
    #         raise ValueError("Currency code must be 3 characters long (e.g., 'KGS')")
    #     return v

    # @validator("countryCode")
    # def validate_country_code(cls, v):
    #     if v and len(v) != 2:
    #         raise ValueError("Country code must be 2 characters long (e.g., 'KG')")
    #     return v

    class Config:
        orm_mode = True

class ESFOut(ESFCreate):
    id: int
    document_uuid: str = None
    status: str
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True
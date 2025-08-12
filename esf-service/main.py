from decimal import Decimal
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from schemas import ApiResponse, InvoiceData, InvoiceDetailOut, InvoiceOut, InvoicesResponse
from tortoise.transactions import in_transaction
from deps import get_current_user_from_auth_service
import httpx
import os
from urllib.parse import urljoin
from models import Contractor, Invoice, PaymentType, Currency, Status, ReceiptType, DeliveryType, LegalPerson, VatTaxType


app = FastAPI(title="ESF Service")


GNS_PROXY = os.getenv("GNS_PROXY")
X_ROAD = os.getenv("X-Road-Client")
ClientUUID = os.getenv("ClientUUID")
Authorization = os.getenv("Authorization")
TIN = os.getenv("USER-TIN")


create_url = urljoin(GNS_PROXY, os.getenv("CREATE_PATH"))
get_url = urljoin(GNS_PROXY, os.getenv("GET_PATH"))
update_url = urljoin(GNS_PROXY, os.getenv("UPDATE_PATH"))
delete_url =urljoin(GNS_PROXY, os.getenv("DELETE_PATH"))


@app.get("/invoices/{invoice_id}", response_model=InvoiceDetailOut)
async def get_invoice(invoice_id: int):    
    invoice = await Invoice.filter(id=invoice_id).select_related(
        "paymentType",
        "currency",
        "status",
        "receiptType",
        "deliveryType",
        "legalPerson",
        "contractor",
        "vatTaxType"
    ).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return invoice


@app.get("/invoices/", response_model=List[InvoiceOut])
async def list_invoices():
    invoices = await Invoice.all()
    return invoices


@app.get("/get_invoices/")
async def get_invoices(documentUuid: Optional[str] = None):
    headers = {
        "X-Road-Client": X_ROAD,
        "ClientUUID": ClientUUID,
        "Authorization": Authorization,
        "USER-TIN": TIN,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(get_url, headers=headers, params={"exchangeCode": documentUuid})
            response.raise_for_status()
            data = response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Ошибка при обращении к внешнему сервису: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Внешний сервис вернул ошибку: {exc.response.text}")

    parsed = InvoicesResponse(**data)

    async with in_transaction() as connection:
        try:
            for inv in parsed.invoices:
                payment_type = await PaymentType.get_or_create(code=inv.paymentType.code, defaults={"name": inv.paymentType.name})
                currency = await Currency.get_or_create(code=inv.currency.code, defaults={"name": inv.currency.name})
                status = await Status.get_or_create(code=inv.status.code, defaults={"name": inv.status.name})
                receipt_type = await ReceiptType.get_or_create(code=inv.receiptType.code, defaults={"name": inv.receiptType.name})
                delivery_type = await DeliveryType.get_or_create(code=inv.deliveryType.code, defaults={"name": inv.deliveryType.name})
                legal_person = await LegalPerson.get_or_create(pin=inv.legalPerson.pin, defaults={
                    "fullName": inv.legalPerson.fullName,
                    "mainFullName": inv.legalPerson.mainFullName,
                    "mainPin": inv.legalPerson.mainPin
                })
                contractor = await Contractor.get_or_create(pin=inv.contractor.pin, defaults={
                    "fullName": inv.contractor.fullName,
                    "mainFullName": inv.contractor.mainFullName,
                    "mainPin": inv.contractor.mainPin
                })
                vat_tax_type = await VatTaxType.get_or_create(code=inv.vatTaxType.code, defaults={
                    "rate": inv.vatTaxType.rate,
                    "name": inv.vatTaxType.name
                })

                print(payment_type[0].id)  # Должен вывести ID
                print(contractor[0].id)   

                await Invoice.update_or_create(
                    documentUuid=inv.documentUuid,
                    defaults={
                        "totalAmount": inv.totalAmount,
                        "createdDate": inv.createdDate,
                        "deliveryDate": inv.deliveryDate,
                        "invoiceDate": inv.invoiceDate,
                        "ownedCrmReceiptCode": inv.ownedCrmReceiptCode,
                        "invoiceNumber": inv.invoiceNumber,
                        "number": inv.number,
                        "note": inv.note,
                        "correctedReceiptUuid": inv.correctedReceiptUuid,
                        "isResident": inv.isResident.lower() == "true" if inv.isResident else None,
                        "paymentType": payment_type[0],
                        "currency": currency[0],
                        "status": status[0],
                        "receiptType": receipt_type[0],
                        "deliveryType": delivery_type[0],
                        "legalPerson": legal_person[0],
                        "contractor": contractor[0],
                        "vatTaxType": vat_tax_type[0]
                    }
                )
        except Exception as e:
            print(f"Ошибка в транзакции: {e}")
            await connection.rollback()

    return {"status": "ok", "saved": len(parsed.invoices)}


@app.post("/process_invoice/", response_model=ApiResponse)
async def process_invoice_data(data: InvoiceData):
    """
    Этот эндпоинт принимает данные, отправляет их на внешний сервис
    и возвращает ответ от него.

    - **Принимает**: JSON объект со структурой `InvoiceData`.
    - **Проксирует**: POST-запрос на http://172.16.0.3:8003/
    - **Возвращает**: Ответ от внешнего сервиса.
    """
    headers = {
        "X-Road-Client": X_ROAD,
        "ClientUUID": ClientUUID,
        "Authorization": Authorization,
        "USER-TIN": TIN,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(create_url, json=data.model_dump(mode='json'), headers=headers)
            response.raise_for_status()

            return response.json()

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Ошибка при обращении к внешнему сервису: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Внешний сервис вернул ошибку: {exc.response.text}"
            )


@app.put("/process_invoice/{id}", response_model=ApiResponse)
async def update_invoice_data(
    id: str,
    data: InvoiceData 
):
    """
    Обновляет документ по ID через внешний сервис.

    - **Принимает**: ID документа и JSON объект `InvoiceData`.
    - **Проксирует**: PUT-запрос на внешний сервис.
    - **Возвращает**: Ответ от внешнего сервиса.
    """
    headers = {
        "X-Road-Client": X_ROAD,
        "ClientUUID": ClientUUID,
        "Authorization": Authorization,
        "USER-TIN": TIN,
        "Content-Type": "application/json"
    }

    # Формируем URL с ID
    url = f"{update_url}/{id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=data.model_dump(mode='json'), headers=headers)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Ошибка при обращении к внешнему сервису: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Внешний сервис вернул ошибку: {exc.response.text}"
            )


@app.delete("/delete_invoice/{invoice_id}")
async def delete_invoice(invoice_id: str):
    headers = {
        "X-Road-Client": X_ROAD,
        "ClientUUID": ClientUUID,
        "Authorization": Authorization,
        "USER-TIN": TIN,
        "Content-Type": "application/json"
    }
    
    # Формируем URL с ID
    url = f"{delete_url}/{invoice_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                url,  
                headers=headers
            )
            response.raise_for_status()

            return {
                "status": "success",
                "deleted_id": invoice_id,
                "external_response": response.json()
            }

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Ошибка при обращении к внешнему сервису: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Внешний сервис вернул ошибку: {exc.response.text}"
            )
    

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@postgres:5432/esf_db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
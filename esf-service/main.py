from decimal import Decimal
from fastapi import FastAPI, Depends, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from schemas import ApiResponse, InvoiceData
from models import ESFModel
from deps import get_current_user_from_auth_service
import httpx
import os
from urllib.parse import urljoin


app = FastAPI(title="ESF Service")


GNS_PROXY = os.getenv("GNS_PROXY")
X_ROAD = os.getenv("X-Road-Client")
ClientUUID = os.getenv("ClientUUID")
Authorization = os.getenv("Authorization")
TIN = os.getenv("USER-TIN")
CREATE_PATH = os.getenv("CREATE_PATH")
GET_PATH = os.getenv("GET_PATH")

create_url = urljoin(GNS_PROXY, CREATE_PATH)
get_url = urljoin(GNS_PROXY, GET_PATH)


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


@app.get("/get_invoices/")
async def get_invoices():
    """
    Этот эндпоинт получает список всех документов по реализации.

    - **Проксирует**: GET-запрос
    - **Возвращает**: Список документов в формате JSON.
    """
    headers = {
        "X-Road-Client": X_ROAD,
        "ClientUUID": ClientUUID,
        "Authorization": Authorization,
        "USER-TIN": TIN,
        "Content-Type": "application/json"
    }
    print(f"GET URL: {get_url}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(get_url, headers=headers, params={"exchangeCode": "d215a809-d2f7-4944-be0a-a15a1fdeaff8"})
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
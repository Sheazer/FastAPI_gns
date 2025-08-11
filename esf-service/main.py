from fastapi import FastAPI, Depends, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from schemas import ESFCreate, ESFOut
from models import ESFDocument
from deps import get_current_user_from_auth_service
import httpx
import os

app = FastAPI(title="ESF Service")

GNS_PROXY = os.getenv("GNS_PROXY", "http://gns-proxy:8003/gns/receive")

@app.post("/esf/", response_model=ESFOut)
async def create_esf(payload: ESFCreate, user = Depends(get_current_user_from_auth_service)):
    doc = await ESFDocument.create(
        document_uuid=payload.document_uuid,
        legal_person_tin=payload.legal_person_tin,
        data=payload.data,
        status="draft",
        created_by=user["id"]
    )
    return ESFOut.from_orm(doc)

@app.get("/esf/", response_model=list[ESFOut])
async def list_esf():
    docs = await ESFDocument.all().order_by("-created_at")
    return [ESFOut.from_orm(d) for d in docs]

@app.get("/esf/{item_id}", response_model=ESFOut)
async def get_esf(item_id: int):
    doc = await ESFDocument.get_or_none(id=item_id)
    if not doc:
        raise HTTPException(404, "Not found")
    return ESFOut.from_orm(doc)

@app.post("/esf/{item_id}/send")
async def send_esf(item_id: int):
    doc = await ESFDocument.get_or_none(id=item_id)
    if not doc:
        raise HTTPException(404, "Not found")
    # отправляем в GNS
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(GNS_PROXY, json={
                "document_uuid": doc.document_uuid,
                "legal_person_tin": doc.legal_person_tin,
                "data": doc.data
            }, timeout=10.0)
            resp.raise_for_status()
        except Exception as e:
            doc.status = "failed"
            await doc.save()
            raise HTTPException(502, f"Failed to send to GNS: {e}")
    # если успешно
    doc.status = "sent"
    await doc.save()
    return {"status": "sent"}

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@postgres:5432/esf_db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

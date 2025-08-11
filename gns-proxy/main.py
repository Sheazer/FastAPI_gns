from fastapi import FastAPI, Request
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI(title="GNS Proxy (mock)")

class ReceiveModel(BaseModel):
    document_uuid: str
    legal_person_tin: str
    data: dict

@app.post("/gns/receive")
async def receive(doc: ReceiveModel):
    # имитация обработки: возвращаем статус и внутренний id
    return {"status": "accepted", "gns_id": str(uuid4())}

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os

security = HTTPBearer()
AUTH_SERVICE = os.getenv("AUTH_SERVICE", "http://auth-service:8001")

async def get_current_user_from_auth_service(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{AUTH_SERVICE}/me", headers=headers, timeout=5.0)
            if resp.status_code != 200:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
            return resp.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Auth service unavailable")

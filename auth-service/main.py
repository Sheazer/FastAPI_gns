from fastapi import FastAPI, Depends, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from auth import create_access_token, get_current_user
from models import User
from schemas import UserCreate, Token, UserOut

app = FastAPI(title="Auth Service")

@app.post("/register", response_model=UserOut)
async def register(data: UserCreate):
    exists = await User.get_or_none(username=data.username)
    if exists:
        raise HTTPException(status_code=400, detail="User exists")
    user = await User.create_user(username=data.username, password=data.password, tin=data.tin)
    return UserOut(id=user.id, username=user.username, tin=user.tin)

@app.post("/login", response_model=Token)
async def login(data: UserCreate):
    user = await User.authenticate(data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid creds")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")

@app.get("/me", response_model=UserOut)
async def me(user=Depends(get_current_user)):
    return UserOut(id=user.id, username=user.username, tin=user.tin)

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@postgres:5432/esf_db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

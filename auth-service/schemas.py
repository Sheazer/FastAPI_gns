from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    tin: str | None = None

class UserOut(BaseModel):
    id: int
    username: str
    tin: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

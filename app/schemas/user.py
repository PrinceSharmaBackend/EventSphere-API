from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "participant"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
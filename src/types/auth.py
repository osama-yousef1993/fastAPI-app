from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    email: EmailStr = Field(min_length=5, description="User's email address")
    password: str = Field(min_length=8)


class User(BaseModel):
    public_id: str
    name: str
    email: EmailStr = Field(min_length=5, description="User's email address")


class ChangePassword(BaseModel):
    public_id: str
    password: str = Field(min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str


class UsersResponse(BaseModel):
    users: list[User]


class VerifyAccountResponse(BaseModel):
    access_token: str
    token_type: str
    detail: str


class DefaultResponse(BaseModel):
    detail: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class VerifyOTP(BaseModel):
    email: str
    user_otp: int

from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: str
    password: str = Field(min_length=8, max_length=128)
    phone: str = ""
    role: str = "Owner"

    @field_validator("email")
    @classmethod
    def email_looks_valid(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Valid email required")
        return value

    @field_validator("password")
    @classmethod
    def password_has_letter_and_number(cls, value: str) -> str:
        if not any(ch.isalpha() for ch in value) or not any(ch.isdigit() for ch in value):
            raise ValueError("Password must include at least one letter and one number")
        return value


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class AuthUserResponse(BaseModel):
    id: int
    company_id: int | None = None
    name: str
    email: str
    phone: str
    role: str
    avatar: str
    is_primary: bool
    terms_accepted: bool = False
    role_key: str | None = None
    permissions: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True

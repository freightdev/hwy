from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[int] = None
    company_id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: str = ""
    role: str = "Owner"
    avatar: str = ""
    is_primary: bool = False

    class Config:
        from_attributes = True


class UserCreate(UserSchema):
    pass


class OnboardingData(BaseModel):
    company: dict
    onboarded: bool = True
    device_id: str = ""
    location_lat: float | None = None
    location_lng: float | None = None
    user_agent: str = ""
    terms_accepted: bool = False

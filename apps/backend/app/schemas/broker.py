from pydantic import BaseModel
from typing import Optional


class BrokerSchema(BaseModel):
    id: Optional[int] = None
    company_id: Optional[int] = None
    name: str = ""
    mc: str = ""
    status: str = "Active"
    loads: int = 0
    revenue: str = ""
    on_time: int = 0
    rating: float = 0
    credit: str = ""
    available: str = ""
    favorite: bool = False
    insurance: bool = True
    authority: bool = True
    website: str = ""
    email: str = ""
    phone: str = ""

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional


class LoadSchema(BaseModel):
    id: str
    company_id: Optional[int] = None
    broker_id: Optional[int] = None
    driver_id: Optional[int] = None
    route: str = ""
    date: str = ""
    rate: str = ""
    rpm: str = ""
    miles: int = 0
    equipment: str = ""
    weight: str = ""
    broker_name: str = ""
    mc: str = ""
    pickup: str = ""
    delivery: str = ""
    stops: int = 1
    status: str = "Available"
    pickup_location: str = ""
    delivery_location: str = ""

    class Config:
        from_attributes = True

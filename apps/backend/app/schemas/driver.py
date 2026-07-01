from pydantic import BaseModel
from typing import Optional


class DriverSchema(BaseModel):
    id: Optional[int] = None
    company_id: Optional[int] = None
    name: str = ""
    truck: str = ""
    phone: str = ""
    email: str = ""
    status: str = "Available"
    route: str = ""
    load_id: Optional[str] = None
    rate: str = ""
    license: str = ""
    doe: str = ""
    on_time: int = 0
    loads_completed: int = 0
    rating: float = 0
    cdl_class: str = "Class A"
    cdl_state: str = ""
    home_base: str = ""

    class Config:
        from_attributes = True


class DriverCreate(BaseModel):
    name: str
    truck: str
    phone: str = ""
    email: str = ""
    status: str = "Available"
    license: str = ""
    doe: str = ""

from pydantic import BaseModel
from typing import Optional, Any


class CompanySchema(BaseModel):
    id: Optional[int] = None
    name: str = ""
    mc: str = ""
    dot: str = ""
    scac: str = ""
    type: str = "For-Hire Carrier"
    role_type: str = "carrier"
    founded: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""
    phone: str = ""
    email: str = ""
    website: str = ""
    fleet_size: int = 0
    trailer_types: list = []
    operating_states: list = []
    description: str = ""
    score: float = 0
    score_factors: Any = {}
    safety: Any = {}
    safety_programs: list = []
    authority: Any = {}
    rating: float = 0
    review_count: int = 0
    show_mock_data: bool = True

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional, Any


class FlowSchema(BaseModel):
    id: Optional[int] = None
    company_id: Optional[int] = None
    name: str = ""
    steps: int = 0
    type: str = "Manual"
    enabled: bool = False
    icon: str = "⚡"
    category: str = ""
    step_details: Any = []

    class Config:
        from_attributes = True

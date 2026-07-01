from pydantic import BaseModel
from typing import Optional, Any


class DocumentSchema(BaseModel):
    id: Optional[int] = None
    company_id: Optional[int] = None
    name: str = ""
    category: str = ""
    expiry: Optional[str] = None
    status: str = "Valid"
    icon: str = "📄"
    size: str = ""
    file_url: Optional[str] = None

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional


class InvoiceSchema(BaseModel):
    id: str
    company_id: Optional[int] = None
    broker_id: Optional[int] = None
    load_id: Optional[str] = None
    broker_name: str = ""
    amount: str = ""
    amount_cents: int = 0
    status: str = "Sent"
    date: str = ""
    due_date: str = ""

    class Config:
        from_attributes = True

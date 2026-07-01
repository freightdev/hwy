from pydantic import BaseModel
from typing import Optional


class PaymentSchema(BaseModel):
    id: Optional[int] = None
    company_id: Optional[int] = None
    from_broker: str = ""
    broker_id: Optional[int] = None
    amount: str = ""
    amount_cents: int = 0
    date: str = ""
    method: str = "ACH"
    status: str = "Received"
    invoice_id: Optional[str] = None

    class Config:
        from_attributes = True

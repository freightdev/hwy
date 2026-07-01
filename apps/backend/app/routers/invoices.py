from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.schemas.invoice import InvoiceSchema
from app.schemas.payment import PaymentSchema

router = APIRouter(prefix="/api/v1/invoices", tags=["invoices"])


@router.get("")
def list_invoices(status: str = Query(None), db: Session = Depends(get_db)):
    q = db.query(Invoice)
    if status:
        q = q.filter(Invoice.status.ilike(f"%{status}%"))
    invoices = q.order_by(Invoice.date.desc()).all()
    return {"data": [InvoiceSchema.model_validate(i).model_dump() for i in invoices]}


@router.get("/payments")
def list_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).order_by(Payment.date.desc()).all()
    return {"data": [PaymentSchema.model_validate(p).model_dump() for p in payments]}


@router.get("/stats")
def invoice_stats(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    total_revenue = sum(i.amount_cents for i in invoices if i.status == "Paid")
    outstanding = sum(i.amount_cents for i in invoices if i.status in ("Sent", "Overdue"))
    return {
        "data": {
            "total_revenue_mtd": f"${total_revenue // 100:,}",
            "outstanding": f"${outstanding // 100:,}",
            "total_revenue_cents": total_revenue,
            "outstanding_cents": outstanding,
        }
    }

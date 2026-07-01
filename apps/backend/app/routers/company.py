from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.models.user import User
from app.models.driver import Driver
from app.models.broker import Broker
from app.models.load import Load
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.models.document import Document
from app.models.flow import Flow
from app.schemas.company import CompanySchema
from app.services.seed import add_seed_data, remove_seed_data
from app.services.auth import get_current_user

router = APIRouter(prefix="/api/v1/company", tags=["company"])


@router.get("")
def get_company(db: Session = Depends(get_db)):
    company = db.query(Company).first()
    if not company:
        raise HTTPException(status_code=404, detail="No company found")
    return {"data": CompanySchema.model_validate(company).model_dump()}


@router.put("")
def update_company(data: CompanySchema, db: Session = Depends(get_db)):
    company = db.query(Company).first()
    if not company:
        raise HTTPException(status_code=404, detail="No company found")
    for key, val in data.model_dump(exclude={"id"}).items():
        setattr(company, key, val)
    db.commit()
    db.refresh(company)
    return {"data": CompanySchema.model_validate(company).model_dump()}


@router.post("/reset")
def reset_company(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    company = db.query(Company).first()
    if not company:
        raise HTTPException(status_code=404, detail="No company found")

    db.query(Flow).filter(Flow.company_id == company.id).delete(synchronize_session=False)
    db.query(Document).filter(Document.company_id == company.id).delete(synchronize_session=False)
    db.query(Payment).filter(Payment.company_id == company.id).delete(synchronize_session=False)
    db.query(Invoice).filter(Invoice.company_id == company.id).delete(synchronize_session=False)
    db.query(Load).filter(Load.company_id == company.id).delete(synchronize_session=False)
    db.query(Broker).filter(Broker.company_id == company.id).delete(synchronize_session=False)
    db.query(Driver).filter(Driver.company_id == company.id).delete(synchronize_session=False)

    db.query(User).filter(User.company_id == company.id).update(
        {User.company_id: None, User.is_primary: False},
        synchronize_session=False,
    )

    db.delete(company)
    db.commit()

    current_user.company_id = None
    current_user.is_primary = False
    db.commit()

    return {"data": {"deleted": True}}


@router.post("/toggle-mock")
def toggle_mock(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    company = db.query(Company).first()
    if not company:
        raise HTTPException(status_code=404, detail="No company found")

    if company.show_mock_data:
        remove_seed_data(db)
        company.show_mock_data = False
        message = "Mock data removed"
    else:
        add_seed_data(db)
        company.show_mock_data = True
        message = "Mock data restored"

    db.commit()
    db.refresh(company)
    return {"data": CompanySchema.model_validate(company).model_dump(), "message": message}

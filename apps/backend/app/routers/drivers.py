from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.driver import Driver
from app.schemas.driver import DriverSchema, DriverCreate

router = APIRouter(prefix="/api/v1/drivers", tags=["drivers"])


@router.get("")
def list_drivers(
    status: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Driver)
    if status and status != "all":
        q = q.filter(Driver.status.ilike(status.replace("-", " ")))
    if search:
        q = q.filter(Driver.name.ilike(f"%{search}%"))
    drivers = q.all()
    return {"data": [DriverSchema.model_validate(d).model_dump() for d in drivers]}


@router.get("/{driver_id}")
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"data": DriverSchema.model_validate(driver).model_dump()}


@router.post("")
def create_driver(data: DriverCreate, db: Session = Depends(get_db)):
    driver = Driver(**data.model_dump())
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return {"data": DriverSchema.model_validate(driver).model_dump()}


@router.delete("/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    db.delete(driver)
    db.commit()
    return {"data": {"deleted": True}}

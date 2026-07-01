from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.load import Load
from app.schemas.load import LoadSchema

router = APIRouter(prefix="/api/v1/loads", tags=["loads"])


@router.get("")
def list_loads(
    search: str = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Load)
    if search:
        q = q.filter(
            Load.route.ilike(f"%{search}%") | Load.broker_name.ilike(f"%{search}%")
        )
    if status:
        q = q.filter(Load.status.ilike(f"%{status}%"))
    loads = q.all()
    return {"data": [LoadSchema.model_validate(l).model_dump() for l in loads]}


@router.get("/{load_id}")
def get_load(load_id: str, db: Session = Depends(get_db)):
    load = db.query(Load).filter(Load.id == load_id).first()
    if not load:
        return {"error": "Load not found"}
    return {"data": LoadSchema.model_validate(load).model_dump()}


@router.post("/{load_id}/book")
def book_load(load_id: str, db: Session = Depends(get_db)):
    return {"error": "Load booking requires carrier API integration (DAT/Truckstop)"}

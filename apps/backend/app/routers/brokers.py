from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.broker import Broker
from app.schemas.broker import BrokerSchema

router = APIRouter(prefix="/api/v1/brokers", tags=["brokers"])


@router.get("")
def list_brokers(
    search: str = Query(None),
    favorites: bool = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Broker)
    if search:
        q = q.filter(Broker.name.ilike(f"%{search}%"))
    if favorites:
        q = q.filter(Broker.favorite == True)
    brokers = q.all()
    return {"data": [BrokerSchema.model_validate(b).model_dump() for b in brokers]}


@router.get("/{broker_id}")
def get_broker(broker_id: int, db: Session = Depends(get_db)):
    broker = db.query(Broker).filter(Broker.id == broker_id).first()
    if not broker:
        return {"error": "Broker not found"}
    return {"data": BrokerSchema.model_validate(broker).model_dump()}


@router.post("/{broker_id}/favorite")
def toggle_favorite(broker_id: int, db: Session = Depends(get_db)):
    broker = db.query(Broker).filter(Broker.id == broker_id).first()
    if not broker:
        return {"error": "Broker not found"}
    broker.favorite = not broker.favorite
    db.commit()
    return {"data": BrokerSchema.model_validate(broker).model_dump()}

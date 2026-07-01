from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.flow import Flow
from app.schemas.flow import FlowSchema

router = APIRouter(prefix="/api/v1/flows", tags=["flows"])


@router.get("")
def list_flows(db: Session = Depends(get_db)):
    flows = db.query(Flow).all()
    return {"data": [FlowSchema.model_validate(f).model_dump() for f in flows]}


@router.post("/{flow_id}/toggle")
def toggle_flow(flow_id: int, db: Session = Depends(get_db)):
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        return {"error": "Flow not found"}
    flow.enabled = not flow.enabled
    db.commit()
    return {"data": FlowSchema.model_validate(flow).model_dump()}


@router.post("/{flow_id}/run")
def run_flow(flow_id: int, db: Session = Depends(get_db)):
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        return {"error": "Flow not found"}
    return {"data": {"running": True, "message": f"Executing {flow.name}..."}}

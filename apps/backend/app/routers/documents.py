from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentSchema

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.get("")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return {"data": [DocumentSchema.model_validate(d).model_dump() for d in docs]}


@router.get("/categories")
def document_categories(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    cats = {}
    for d in docs:
        cat = d.category or "Other"
        if cat not in cats:
            cats[cat] = 0
        cats[cat] += 1
    return {
        "data": [
            {"name": k, "count": v} for k, v in sorted(cats.items())
        ]
    }

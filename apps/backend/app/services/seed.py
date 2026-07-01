"""Seed the database with mock data on first startup."""
import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User
from app.models.driver import Driver
from app.models.broker import Broker
from app.models.load import Load
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.models.document import Document
from app.models.flow import Flow


MOCK_DIR = Path("/data/mock") if Path("/data/mock").exists() else Path(__file__).resolve().parents[3] / "dataset" / "mock"

SEED_COMPANY_IDS = [1]
SEED_USER_IDS = [1, 2, 3]
SEED_DRIVER_IDS = [1, 2, 3, 4, 5, 6]
SEED_BROKER_IDS = [1, 2, 3, 4, 5, 6, 7, 8]
SEED_LOAD_IDS = ["L10025", "L10026", "L10027", "L10028", "L10029", "L10030"]
SEED_INVOICE_IDS = ["INV-2025-1068", "INV-2025-1065", "INV-2025-1064", "INV-2025-1063", "INV-2025-1062", "INV-2025-1061"]
SEED_PAYMENT_IDS = [1, 2, 3, 4]
SEED_DOCUMENT_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
SEED_FLOW_IDS = [1, 2, 3, 4, 5, 6, 7]


def _load_json(name):
    path = MOCK_DIR / name
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)


def _filter_fields(model_cls, data):
    cols = {c.name for c in model_cls.__table__.columns}
    return {k: v for k, v in data.items() if k in cols}


def _seed_model(db, model_cls, name, transform=None):
    for item in _load_json(name):
        record = model_cls(**_filter_fields(model_cls, item))
        if transform:
            transform(record)
        db.add(record)
    db.flush()


def add_seed_data(db: Session):
    _seed_model(db, Driver, "drivers.json")
    _seed_model(db, Broker, "brokers.json")
    _seed_model(db, Load, "loads.json")
    _seed_model(db, Invoice, "invoices.json")
    _seed_model(db, Payment, "payments.json")
    _seed_model(db, Document, "documents.json")
    _seed_model(db, Flow, "flows.json")
    db.commit()


def remove_seed_data(db: Session):
    db.query(Flow).filter(Flow.id.in_(SEED_FLOW_IDS)).delete(synchronize_session=False)
    db.query(Document).filter(Document.id.in_(SEED_DOCUMENT_IDS)).delete(synchronize_session=False)
    db.query(Payment).filter(Payment.id.in_(SEED_PAYMENT_IDS)).delete(synchronize_session=False)
    db.query(Invoice).filter(Invoice.id.in_(SEED_INVOICE_IDS)).delete(synchronize_session=False)
    db.query(Load).filter(Load.id.in_(SEED_LOAD_IDS)).delete(synchronize_session=False)
    db.query(Broker).filter(Broker.id.in_(SEED_BROKER_IDS)).delete(synchronize_session=False)
    db.query(Driver).filter(Driver.id.in_(SEED_DRIVER_IDS)).delete(synchronize_session=False)
    db.commit()


def seed_database(db: Session):
    if db.query(Company).count() > 0:
        return

    _seed_model(db, Company, "companies.json")

    from app.services.auth import hash_password

    def hash_user(u):
        u.password_hash = hash_password("password123")
        u.terms_accepted = True

    _seed_model(db, User, "users.json", transform=hash_user)
    add_seed_data(db)
    print("Database seeded successfully from mock data.")

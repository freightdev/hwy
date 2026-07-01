from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(50), primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    broker_id = Column(Integer, ForeignKey("brokers.id", ondelete="SET NULL"), nullable=True)
    load_id = Column(String(50), ForeignKey("loads.id", ondelete="SET NULL"), nullable=True)
    broker_name = Column(String(255), default="")
    amount = Column(String(50), default="")
    amount_cents = Column(BigInteger, default=0)
    status = Column(String(50), default="Sent")
    date = Column(String(50), default="")
    due_date = Column(String(50), default="")

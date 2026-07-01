from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    from_broker = Column(String(255), default="")
    broker_id = Column(Integer, ForeignKey("brokers.id", ondelete="SET NULL"), nullable=True)
    amount = Column(String(50), default="")
    amount_cents = Column(BigInteger, default=0)
    date = Column(String(50), default="")
    method = Column(String(50), default="ACH")
    status = Column(String(50), default="Received")
    invoice_id = Column(String(50), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True)

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Load(Base):
    __tablename__ = "loads"

    id = Column(String(50), primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    broker_id = Column(Integer, ForeignKey("brokers.id", ondelete="SET NULL"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True)
    route = Column(String, default="")
    date = Column(String(50), default="")
    rate = Column(String(50), default="")
    rpm = Column(String(50), default="")
    miles = Column(Integer, default=0)
    equipment = Column(String(100), default="")
    weight = Column(String(50), default="")
    broker_name = Column(String(255), default="")
    mc = Column(String(50), default="")
    pickup = Column(String(50), default="")
    delivery = Column(String(50), default="")
    stops = Column(Integer, default=1)
    status = Column(String(50), default="Available")
    pickup_location = Column(String(255), default="")
    delivery_location = Column(String(255), default="")

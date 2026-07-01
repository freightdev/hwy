from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.database import Base


class Broker(Base):
    __tablename__ = "brokers"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(255), default="")
    mc = Column(String(50), default="")
    status = Column(String(50), default="Active")
    loads = Column(Integer, default=0)
    revenue = Column(String(50), default="")
    on_time = Column(Integer, default=0)
    rating = Column(Float, default=0)
    credit = Column(String(50), default="")
    available = Column(String(50), default="")
    favorite = Column(Boolean, default=False)
    insurance = Column(Boolean, default=True)
    authority = Column(Boolean, default=True)
    website = Column(String(255), default="")
    email = Column(String(255), default="")
    phone = Column(String(50), default="")

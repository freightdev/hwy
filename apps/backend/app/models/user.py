from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(255), default="")
    email = Column(String(255), default="")
    phone = Column(String(50), default="")
    role = Column(String(50), default="Owner")
    avatar = Column(String(500), default="")
    is_primary = Column(Boolean, default=False)
    password_hash = Column(String(255), default="")
    device_id = Column(String(255), default="")
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    user_agent = Column(String(500), default="")
    ip_address = Column(String(45), default="")
    terms_accepted = Column(Boolean, default=False)

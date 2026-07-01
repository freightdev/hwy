from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON, ARRAY
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), default="")
    mc = Column(String(50), default="")
    dot = Column(String(50), default="")
    scac = Column(String(10), default="")
    type = Column(String(50), default="For-Hire Carrier")
    role_type = Column(String(20), default="carrier")
    founded = Column(String(50), default="")
    address = Column(String(255), default="")
    city = Column(String(100), default="")
    state = Column(String(10), default="")
    zip = Column(String(20), default="")
    phone = Column(String(50), default="")
    email = Column(String(255), default="")
    website = Column(String(255), default="")
    fleet_size = Column(Integer, default=0)
    trailer_types = Column(ARRAY(String), default=[])
    operating_states = Column(ARRAY(String), default=[])
    description = Column(Text, default="")
    score = Column(Float, default=0)
    score_factors = Column(JSON, default={})
    safety = Column(JSON, default={})
    safety_programs = Column(ARRAY(String), default=[])
    authority = Column(JSON, default={})
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    show_mock_data = Column(Boolean, default=True)

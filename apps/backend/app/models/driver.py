from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(255), default="")
    truck = Column(String(50), default="")
    phone = Column(String(50), default="")
    email = Column(String(255), default="")
    status = Column(String(50), default="Available")
    route = Column(String, default="")
    load_id = Column(String(50), nullable=True)
    rate = Column(String(50), default="")
    license = Column(String(100), default="")
    doe = Column(String(50), default="")
    on_time = Column(Integer, default=0)
    loads_completed = Column(Integer, default=0)
    rating = Column(Float, default=0)
    cdl_class = Column(String(20), default="Class A")
    cdl_state = Column(String(10), default="")
    home_base = Column(String(255), default="")

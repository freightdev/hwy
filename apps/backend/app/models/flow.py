from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey
from app.database import Base


class Flow(Base):
    __tablename__ = "flows"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(255), default="")
    steps = Column(Integer, default=0)
    type = Column(String(50), default="Manual")
    enabled = Column(Boolean, default=False)
    icon = Column(String(10), default="⚡")
    category = Column(String(100), default="")
    step_details = Column(JSON, default=[])

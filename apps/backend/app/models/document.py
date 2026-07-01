from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(255), default="")
    category = Column(String(100), default="")
    expiry = Column(String(50), nullable=True)
    status = Column(String(50), default="Valid")
    icon = Column(String(10), default="📄")
    size = Column(String(20), default="")
    file_url = Column(Text, nullable=True)

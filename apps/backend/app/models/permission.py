from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint

from app.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (
        UniqueConstraint("role_key", "permission_key", name="uq_role_permission"),
    )

    id = Column(Integer, primary_key=True, index=True)
    role_key = Column(String(50), index=True, nullable=False)
    permission_key = Column(String(100), index=True, nullable=False)
    allowed = Column(Boolean, default=False, nullable=False)

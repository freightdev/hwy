from pydantic import BaseModel


class PermissionUpdate(BaseModel):
    allowed: bool


class UserRoleUpdate(BaseModel):
    role: str

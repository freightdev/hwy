from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.permission import RolePermission
from app.models.user import User
from app.schemas.admin import PermissionUpdate, UserRoleUpdate
from app.schemas.auth import AuthUserResponse
from app.services.auth import get_current_user
from app.services.permissions import DEFAULT_ALLOWED, PERMISSIONS, ROLES, normalize_role, permission_keys_for_role

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


def _permission_overrides(db: Session) -> dict[str, dict[str, bool]]:
    rows = db.query(RolePermission).all()
    grouped: dict[str, dict[str, bool]] = defaultdict(dict)
    for row in rows:
        grouped[row.role_key][row.permission_key] = row.allowed
    return grouped


def _require_admin(current_user: User = Depends(get_current_user)) -> User:
    if normalize_role(current_user.role) != "admin" and not current_user.is_primary:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


def seed_role_permissions(db: Session) -> None:
    existing = {
        (row.role_key, row.permission_key): row
        for row in db.query(RolePermission).all()
    }
    changed = False
    for role in ROLES:
        for permission in PERMISSIONS:
            key = (role.key, permission.key)
            if key in existing:
                continue
            db.add(RolePermission(
                role_key=role.key,
                permission_key=permission.key,
                allowed=permission.key in DEFAULT_ALLOWED.get(role.key, set()),
            ))
            changed = True
    if changed:
        db.commit()


def user_response(user: User, db: Session) -> dict:
    overrides = _permission_overrides(db)
    data = AuthUserResponse.model_validate(user).model_dump()
    data["role_key"] = normalize_role(user.role)
    data["permissions"] = permission_keys_for_role(user.role, overrides.get(normalize_role(user.role), {}))
    return data


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(_require_admin),
):
    users = db.query(User).order_by(User.id.asc()).all()
    return {"data": {"users": [user_response(user, db) for user in users]}}


@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(_require_admin),
):
    role_key = normalize_role(data.role)
    if role_key not in {role.key for role in ROLES}:
        raise HTTPException(status_code=422, detail="Unknown role")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id and normalize_role(user.role) == "admin" and role_key != "admin":
        raise HTTPException(status_code=400, detail="Admins cannot remove their own admin role")
    label = next(role.label for role in ROLES if role.key == role_key)
    user.role = label
    db.commit()
    db.refresh(user)
    return {"data": {"user": user_response(user, db)}}


@router.get("/permissions")
def get_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(_require_admin),
):
    seed_role_permissions(db)
    overrides = _permission_overrides(db)
    roles_payload = []
    for role in ROLES:
        count = db.query(User).filter(User.role.ilike(role.label)).count()
        roles_payload.append({
            "key": role.key,
            "label": role.label,
            "description": role.description,
            "locked": role.locked,
            "member_count": count,
            "permissions": permission_keys_for_role(role.key, overrides.get(role.key, {})),
        })
    permissions_payload = [permission.__dict__ for permission in PERMISSIONS]
    return {"data": {"roles": roles_payload, "permissions": permissions_payload}}


@router.patch("/permissions/{role_key}/{permission_key}")
def update_permission(
    role_key: str,
    permission_key: str,
    data: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(_require_admin),
):
    role_key = normalize_role(role_key)
    if role_key == "admin":
        raise HTTPException(status_code=400, detail="Admin permissions are locked")
    if role_key not in {role.key for role in ROLES}:
        raise HTTPException(status_code=404, detail="Role not found")
    if permission_key not in {permission.key for permission in PERMISSIONS}:
        raise HTTPException(status_code=404, detail="Permission not found")
    row = db.query(RolePermission).filter(
        RolePermission.role_key == role_key,
        RolePermission.permission_key == permission_key,
    ).first()
    if not row:
        row = RolePermission(role_key=role_key, permission_key=permission_key, allowed=data.allowed)
        db.add(row)
    else:
        row.allowed = data.allowed
    db.commit()
    return {"data": {"role_key": role_key, "permission_key": permission_key, "allowed": row.allowed}}

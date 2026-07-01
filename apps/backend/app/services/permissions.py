from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoleDefinition:
    key: str
    label: str
    description: str
    locked: bool = False


@dataclass(frozen=True)
class PermissionDefinition:
    key: str
    label: str
    group: str
    description: str


ROLES = [
    RoleDefinition("admin", "Admin", "Owns HWY account setup, people, billing, integrations, and all permissions.", True),
    RoleDefinition("owner", "Owner", "Runs company operations and can manage dispatch, team, billing, and settings."),
    RoleDefinition("dispatcher", "Dispatcher", "Moves loads, assigns drivers, manages brokers, and runs daily operations."),
    RoleDefinition("driver", "Driver", "Uses mobile tools for assigned loads, documents, messages, and logbook work."),
    RoleDefinition("accounting", "Accounting", "Handles invoices, payments, settlements, and financial documents."),
    RoleDefinition("viewer", "Viewer", "Read-only stakeholder access for reporting and oversight."),
]

PERMISSIONS = [
    PermissionDefinition("manage_users", "Manage users", "Admin", "Invite users, edit profiles, assign roles, and deactivate access."),
    PermissionDefinition("manage_permissions", "Manage permissions", "Admin", "Change role access except locked admin permissions."),
    PermissionDefinition("manage_company", "Manage company", "Company", "Edit company profile, authority, equipment, and operating settings."),
    PermissionDefinition("dispatch_loads", "Dispatch loads", "Operations", "Create, assign, update, and close load work."),
    PermissionDefinition("manage_drivers", "Manage drivers", "Operations", "Edit driver records, equipment, status, and assignments."),
    PermissionDefinition("manage_brokers", "Manage brokers", "Network", "Manage broker network and broker scorecards."),
    PermissionDefinition("manage_documents", "Manage documents", "Compliance", "Upload, review, and expire compliance documents."),
    PermissionDefinition("manage_payments", "Manage payments", "Finance", "Create invoices, record payments, and review revenue."),
    PermissionDefinition("use_codriver", "Use CoDriver", "AI", "Use CoDriver runtime console and AI operating workflows."),
    PermissionDefinition("view_reports", "View reports", "Reports", "View dashboards, reports, logbook summaries, and analytics."),
]

DEFAULT_ALLOWED = {
    "admin": {p.key for p in PERMISSIONS},
    "owner": {"manage_users", "manage_company", "dispatch_loads", "manage_drivers", "manage_brokers", "manage_documents", "manage_payments", "use_codriver", "view_reports"},
    "dispatcher": {"dispatch_loads", "manage_drivers", "manage_brokers", "manage_documents", "use_codriver", "view_reports"},
    "driver": {"manage_documents", "use_codriver"},
    "accounting": {"manage_documents", "manage_payments", "view_reports"},
    "viewer": {"view_reports"},
}

ROLE_ALIASES = {
    "admin": "admin",
    "administrator": "admin",
    "owner": "owner",
    "primary": "owner",
    "fleet manager": "owner",
    "operations manager": "dispatcher",
    "dispatcher": "dispatcher",
    "driver": "driver",
    "owner-operator": "owner",
    "accounting": "accounting",
    "viewer": "viewer",
}


def normalize_role(role: str | None) -> str:
    value = (role or "viewer").strip().lower()
    return ROLE_ALIASES.get(value, value if value in {r.key for r in ROLES} else "viewer")


def permission_keys_for_role(role: str, overrides: dict[str, bool] | None = None) -> list[str]:
    role_key = normalize_role(role)
    if role_key == "admin":
        return [p.key for p in PERMISSIONS]
    allowed = set(DEFAULT_ALLOWED.get(role_key, set()))
    for key, is_allowed in (overrides or {}).items():
        if is_allowed:
            allowed.add(key)
        else:
            allowed.discard(key)
    return sorted(allowed)

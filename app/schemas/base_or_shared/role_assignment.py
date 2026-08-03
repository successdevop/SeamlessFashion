from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.org_enums import RoleScope
from app.schemas.identity.user import UserResponse
from app.schemas.organisation.organisation import OrganisationMemberBase


class PermissionBase(BaseModel):
    code: str
    module: str
    resource: str
    action: str
    description: str | None = None


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: UUID


class RoleBase(BaseModel):
    name: str
    description: str | None = None
    scope: RoleScope

    hierarchy_level: int = 1  # Hierarchy level (1 = highest)

    is_system_role: bool = False
    is_assignable_role: bool = True


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: UUID


class RolePermissionDetails(BaseModel):
    role_id: UUID
    permission_id: UUID
    assigned_by: UUID

    role: RoleResponse
    permission: PermissionResponse
    assigner: OrganisationMemberBase


class PermissionDetails(BaseModel):
    roles: list[RolePermissionDetails] = Field(default_factory=list)


class RoleAssignmentBase(BaseModel):
    user_id: UUID
    organisation_id: UUID
    assigned_by: UUID
    assigned_at: datetime
    valid_from: datetime
    valid_until: datetime | None = None
    is_active: bool = True


class RoleAssignmentCreate(RoleAssignmentBase):
    pass


class RoleAssignmentResponse(RoleAssignmentBase):
    id: UUID


class RoleAssignmentDetails(RoleAssignmentResponse):
    membership: OrganisationMemberBase
    role: RoleResponse
    user: UserResponse
    assigned_by_user: UserResponse


class RoleDetails:
    permissions: list[RolePermissionDetails] = Field(default_factory=list)
    role_assignments: list[RoleAssignmentResponse] = Field(default_factory=list)
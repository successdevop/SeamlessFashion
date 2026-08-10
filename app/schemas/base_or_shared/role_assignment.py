from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from app.enums.org_enums import RoleScope
from app.schemas.base_or_shared.orm_base import ORMBaseSchema

if TYPE_CHECKING:
    from app.schemas.organisation.organisation import OrganisationMemberSummary


class PermissionBase(ORMBaseSchema):
    code: str


class PermissionSummary(PermissionBase):
    module: str
    resource: str
    action: str
    description: str | None = None


class PermissionCreate(PermissionSummary):
    pass


class PermissionRead(PermissionSummary):
    id: UUID


class AdminPermissionRead(PermissionRead):
    created_by: UUID


class RoleBase(ORMBaseSchema):
    display_name: str
    name: str
    description: str | None = None
    scope: RoleScope


class RoleSummary(RoleBase):
    hierarchy_level: int = Field(default=1, ge=1, le=50)  # Hierarchy level (1 = highest)


class RoleCreate(RoleSummary):
    pass


class RoleRead(RoleBase):
    id: UUID
    created_by: UUID


class AdminRoleRead(RoleRead):
    is_system_role: bool = False
    is_assignable_role: bool = True


class RolePermissionDetails(ORMBaseSchema):
    role_id: UUID
    permission_id: UUID
    assigned_by: UUID

    role: RoleSummary
    permission: PermissionSummary
    assigner: "OrganisationMemberSummary"


class RoleAssignmentBase(ORMBaseSchema):
    user_id: UUID
    organisation_id: UUID
    assigned_by: UUID


class RoleAssignmentSummary(RoleAssignmentBase):
    assigned_at: datetime
    valid_from: datetime
    valid_until: datetime | None = None
    is_active: bool = True


class RoleAssignmentCreate(RoleAssignmentSummary):
    pass


class RoleAssignmentRead(RoleAssignmentSummary):
    id: UUID


class AdminRoleAssignmentDetails(ORMBaseSchema):
    role_assignment_details: RoleAssignmentRead
    role_permission_details: RolePermissionDetails

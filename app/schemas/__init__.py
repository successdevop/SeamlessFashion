from pydantic import BaseModel
from app.schemas.base_or_shared.address import AddressBase, AddressUpdate, AddressResponse
from app.schemas.base_or_shared.role_assignment import PermissionBase, PermissionCreate, PermissionResponse, RoleBase, \
    RoleCreate, RoleResponse, RolePermissionDetails, RoleAssignmentBase, PermissionDetails, RoleAssignmentCreate, \
    RoleAssignmentResponse, RoleAssignmentDetails, RoleDetails
from app.schemas.identity.user import VerificationDocument, VerificationBase, VerificationCreate, VerificationReview, \
    LoginEventData, LoginEventResponse, UserDetails, UserAddressResponse, UserResponse, AdminUserUpdate, UserCreate, \
    UserProfileUpdate, UserBase, UserSecurityResponse, UserSecurityProfile
from app.schemas.organisation.organisation import OrganisationMemberBase, OrganisationBase, OrganisationCreate, \
    OrganisationResponse, OrganisationDetails, AdminOrganisationMemberDetails
from app.schemas.organisation.store import StoreStaffBase, StoreBase, StoreCreate, StoreUpdate, AdminStoreDetails, \
    StoreResponse, AdminStoreStaffDetails
from app.schemas.organisation.warehouse import WarehouseStaffBase, WarehouseBase, WarehouseCreate, WarehouseUpdate, \
    WarehouseResponse, AdminWarehouseDetails, AdminWarehouseStaffDetails

__all__ = [
    "BaseModel",
    "AddressBase",
    "AddressUpdate",
    "AddressResponse",
    "PermissionBase",
    "PermissionCreate",
    "PermissionResponse",
    "RoleBase",
    "RoleCreate",
    "RoleResponse",
    "RolePermissionDetails",
    "PermissionDetails",
    "RoleAssignmentBase",
    "RoleAssignmentCreate",
    "RoleAssignmentResponse",
    "RoleAssignmentDetails",
    "RoleDetails",
    "VerificationDocument",
    "VerificationBase",
    "VerificationCreate",
    "VerificationReview",
    "LoginEventData",
    "LoginEventResponse",
    "UserSecurityProfile",
    "UserSecurityResponse",
    "UserBase",
    "UserCreate",
    "UserProfileUpdate",
    "AdminUserUpdate",
    "UserResponse",
    "UserAddressResponse",
    "UserDetails",
    "OrganisationMemberBase",
    "OrganisationBase",
    "OrganisationCreate",
    "OrganisationResponse",
    "OrganisationDetails",
    "AdminOrganisationMemberDetails",
    "StoreStaffBase",
    "StoreBase",
    "StoreCreate",
    "StoreUpdate",
    "StoreResponse",
    "AdminStoreDetails",
    "AdminStoreStaffDetails",
    "WarehouseStaffBase",
    "WarehouseBase",
    "WarehouseCreate",
    "WarehouseUpdate",
    "WarehouseResponse",
    "AdminWarehouseDetails",
    "AdminWarehouseStaffDetails"
]

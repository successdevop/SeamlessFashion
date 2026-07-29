from enum import Enum


class SubscriptionStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"


class SubscriptionPlanEnum(str, Enum):
    TRIAL = "trial"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class StoreStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"


class WarehouseStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    CLOSED = "closed"


class MembershipStatus(str, Enum):
    INVITED = "invited"
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    LEFT = "left"
    REMOVED = "removed"


class StaffAssignmentStatus(str, Enum):
    ACTIVE = "active"
    REMOVED = "removed"
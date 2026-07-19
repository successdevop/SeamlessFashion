from enum import Enum


class UserRoleEnum(str, Enum):
    CUSTOMER = "customer"
    PLATFORM_ADMIN = "platform_admin"


class AddressTypeEnum(str, Enum):
    HOME = "home_address"
    OFFICE = "office_address"
    SHIPPING = "shipping_address"
    BILLING = "billing_address"


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
from enum import Enum


class UserRoleEnum(str, Enum):
    CUSTOMER = "customer"
    PLATFORM_ADMIN = "platform_admin"
    DELIVERY_PARTNER = "delivery_partner"
    STORE_MANAGER = "store_manager"
    INVENTORY_MANAGER = "inventory_manager"
    WAREHOUSE_MANAGER = "warehouse_manager"
    PRODUCT_MANAGER = "product_manager"
    CUSTOMER_SUPPORT = "customer_support"
    SALES_REPRESENTATIVE = "sales_representative"
    ORGANISATION_OWNER = "organisation_owner"


class AddressTypeEnum(str, Enum):
    HOME = "home_address"
    OFFICE = "office_address"
    SHIPPING = "shipping_address"
    BILLING = "billing_address"


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
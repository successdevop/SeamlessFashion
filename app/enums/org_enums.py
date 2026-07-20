from enum import Enum


class OrganisationRoleEnum(str, Enum):
    DELIVERY_PARTNER = "delivery_partner"
    STORE_MANAGER = "store_manager"
    INVENTORY_MANAGER = "inventory_manager"
    WAREHOUSE_MANAGER = "warehouse_manager"
    PRODUCT_MANAGER = "product_manager"
    CUSTOMER_SUPPORT = "customer_support"
    SALES_REPRESENTATIVE = "sales_representative"
    ORGANISATION_OWNER = "organisation_owner"
    
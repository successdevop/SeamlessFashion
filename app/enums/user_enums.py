from enum import Enum


class VerificationStatusEnum(str, Enum):
    NOT_STARTED = "not_started"
    DOCUMENTS_UPLOADED = "documents_uploaded"
    PENDING_REVIEW = "pending_review"
    UNDER_REVIEW = "under_review"
    ADDITIONAL_INFO_REQUIRED = "additional_info_required"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"
    FLAGGED_FOR_FRAUD = "flagged_for_fraud"


class DocumentTypeEnum(str, Enum):
    PASSPORT = "passport"
    NATIONAL_ID = "national_id"
    BANK_VERIFICATION_NO = "bank_verification_no"
    DRIVERS_LICENSE = "drivers_license"
    UTILITY_BILL = "utility_bill"
    SELFIE = "selfie"
    BANK_STATEMENT = "bank_statement"
    VOTER_CARD = "voters_card"
    RESIDENCE_PERMIT = "residence_permit"
    INTERNATIONAL_PASSPORT = "international_passport"
    BUSINESS_REGISTRATION_DOCUMENT = "business_registration_document"


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
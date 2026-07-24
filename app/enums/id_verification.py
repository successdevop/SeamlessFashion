from enum import Enum


class VerificationStatuEnum(str, Enum):
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

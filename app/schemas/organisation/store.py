from uuid import UUID

from pydantic import BaseModel

from app.schemas.base_or_shared.common import AddressData, StoreSharedInfo, OrganisationSharedInfo


class Store(BaseModel):
    base: StoreSharedInfo
    updated_by: UUID

    address_id: UUID
    address: AddressData

    organisation_id: UUID
    organisation: OrganisationSharedInfo
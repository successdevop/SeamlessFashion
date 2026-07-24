from uuid import UUID

from pydantic import BaseModel

from app.schemas.base_or_shared.common import AddressData, OrganisationSharedInfo, WareHouseSharedInfo


class WareHouse(BaseModel):
    base: WareHouseSharedInfo
    created_by: UUID
    manager: UUID

    address: AddressData

    organisation_id: UUID
    organisation: OrganisationSharedInfo
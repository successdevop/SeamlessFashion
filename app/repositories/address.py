from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Address
from app.repositories.base import BaseRepository
from app.schemas.base_or_shared.address import AddressCreate


class AddressRepository(BaseRepository[Address]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Address, session=session)

    def create_address(self, address: AddressCreate):
        address_dict = address.model_dump(exclude_unset=True)
        new_address = self.model(**address_dict)

        self.save(new_address)
        self.session.flush()
from idlelib.configdialog import changes

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.address.model import Address
from app.modules.address.repository import AddressRepository
from app.modules.address.schema import AddressRead, AddressCreate, AddressUpdate
from app.modules.users.model import User


class AddressService:
    def __init__(self, db:Session):
        self.address_repository = AddressRepository(db)
    def _dump_address(self,address:Address)->AddressRead:
        return AddressRead.model_validate(address)
    def list_my_addresses(self, current_user:User)->list[AddressRead]:
        user_id=current_user.id
        addresses = self.address_repository.get_address_by_user_id(user_id)
        return [self._dump_address(address) for address in addresses]
    def get_address(self, current_user:User, address_id:int)->AddressRead:
        user_id=current_user.id
        db_address=self.address_repository.get_address_by_id(address_id)
        if db_address is None or db_address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        return self._dump_address(db_address)
    def create_address(self, current_user:User, payload:AddressCreate)->AddressRead:
        user_id=current_user.id
        if payload.is_default:
            self.address_repository.unset_default_for_user(user_id)
        address=Address(
            user_id=user_id,
            **payload.model_dump()
        )

        db_address= self.address_repository.create_address(address)
        return self._dump_address(db_address)
    def update_address(self, current_user:User, address_id:int, payload:AddressUpdate)->AddressRead:
        user_id= current_user.id
        address = self.address_repository.get_address_by_id(address_id)
        if address is None or address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        changes=payload.model_dump(exclude_unset=True, exclude_none=True)

        if changes.get("is_default"):
            self.address_repository.unset_default_for_user(user_id)

        for field,value in changes.items():
            setattr(address, field, value)
        db_address = self.address_repository.update_address(address)
        return self._dump_address(db_address)

    def delete_address(self, address_id:int, current_user:User):
        user_id = current_user.id
        db_address = self.address_repository.get_address_by_id(address_id)
        if db_address is None or db_address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        self.address_repository.delete_address(db_address)


from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.dependency import get_current_user, get_db
from app.modules.address.model import Address
from app.modules.address.schema import AddressRead, AddressCreate, AddressUpdate
from app.modules.address.service import AddressService
from app.modules.users.model import User

router = APIRouter(prefix="/address")

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AddressRead])
def list_my_addresses(current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    address_service = AddressService(db)
    addresses = address_service.list_my_addresses(current_user)
    return addresses

@router.get("/{address_id}", status_code=status.HTTP_200_OK, response_model=AddressRead)
def get_address_by_id(address_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    address_service = AddressService(db)
    address= address_service.get_address(current_user, address_id)
    return address

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AddressRead)
def create_address(payload:AddressCreate, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    address_service = AddressService(db)
    return address_service.create_address(current_user, payload)

@router.patch("/{address_id}", status_code=status.HTTP_200_OK, response_model=AddressRead)
def update_address(payload:AddressUpdate, address_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    address_service = AddressService(db)
    return address_service.update_address(current_user, address_id, payload)

@router.delete("/{address_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_address(address_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    address_service = AddressService(db)
    address_service.delete_address(address_id, current_user)
    return {
        "msg":"address successfully deleted"
    }


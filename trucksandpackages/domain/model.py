from datetime import date
from decimal import Decimal
from typing import Set


class Package:

    def __init__(
        self,
        shipping_type: str,
        weight: Decimal,
        shipping_date: date,
        package_id: str = None,
        carrier_id: str = None
    ):
        self._shipping_type = shipping_type
        self._weight = weight
        self._shipping_date = shipping_date
        self._package_id = package_id
        self._carrier_id = carrier_id

    @property
    def shipping_type(self) -> str:
        return self._shipping_type

    @shipping_type.setter
    def shipping_type(self, shipping_type):
        self._shipping_type = shipping_type
    
    @property
    def weight(self) -> Decimal:
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight
    
    @property
    def shipping_date(self) -> date:
        return self._shipping_date

    @shipping_date.setter
    def shipping_date(self, shipping_date):
        self._shipping_date = shipping_date
    
    @property
    def package_id(self) -> str:
        return self._package_id

    @package_id.setter
    def package_id(self, package_id):
        self._package_id = package_id

    @property
    def carrier_id(self):
        return self._carrier_id

    @carrier_id.setter
    def carrier_id(self, new_carrier_id):
        self._carrier_id = new_carrier_id

    def __eq__(self, other_package) -> bool:
        return self._package_id == other_package.package_id

    def __hash__(self) -> int:
        return hash(self._package_id)

class Truck:

    def __init__(
        self,
        truck_type: str,
        truck_length: int,
        axles: int,
        owner: str,
        truck_id: str = None,
    ):
        self._truck_type = truck_type
        self._truck_length = truck_length
        self._axles = axles
        self._owner = owner
        self._truck_id = truck_id
        self._package_ids: Set[str] = set()

    @property
    def truck_type(self) -> str:
        return self._truck_type

    @truck_type.setter
    def truck_type(self, truck_type: str):
        self._truck_type = truck_type
    
    @property
    def truck_length(self) -> int:
        return self._truck_length

    @truck_length.setter
    def truck_length(self, truck_length: int):
        self._truck_length = truck_length
    
    @property
    def axles(self) -> int:
        return self._axles

    @axles.setter
    def axles(self, axles: int):
        self._axles = axles

    @property
    def truck_id(self) -> str:
        return self._truck_id

    @truck_id.setter
    def truck_id(self, truck_id: str):
        self._truck_id = truck_id
    
    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, auth_id: str):
        self.owner = auth_id

    @property
    def package_ids(self) -> Set[str]:
        return self._package_ids

    def has_packages(self):
        return len(self._package_ids) > 0

    def assign_package_id(self, package_id: str):
        if self._can_assign_package_id(package_id):
            self._package_ids.add(package_id)

    def _can_assign_package_id(self, package_id: str):
        return package_id not in self._package_ids

    def unassign_package_id(self, package_id: str):
        if package_id in self._package_ids:
            self._package_ids.remove(package_id)


class User:

    def __init__(
        self,
        auth_id: str,
        user_id: str = None,
    ):
        self._auth_id = auth_id
        self._user_id = user_id
        self._truck_ids: Set[str] = set()

    @property
    def auth_id(self) -> str:
        return self._auth_id

    @auth_id.setter
    def auth_id(self, auth_id: str):
        self._auth_id = auth_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        self._user_id = user_id

    @property
    def truck_ids(self) -> Set[str]:
        return self._truck_ids

    def has_assigned_trucks(self):
        return len(self._truck_ids) > 0

    def assign_truck(self, truck_id: str):
        if self._can_assign_truck_id(truck_id):
            self._truck_ids.add(truck_id)

    def _can_assign_truck_id(self, truck_id: str):
        return truck_id not in self._truck_ids

    def unassign_truck(self, truck_id: str):
        if truck_id in self._truck_ids:
            self._truck_ids.remove(truck_id)

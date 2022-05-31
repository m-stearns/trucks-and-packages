from datetime import date
from decimal import Decimal
from typing import List, Set


class Package:

    def __init__(
        self,
        shipping_type: str,
        weight: Decimal,
        shipping_date: date,
        package_id: str = None,
        carrier = None
    ):
        self._shipping_type = shipping_type
        self._weight = weight
        self._shipping_date = shipping_date
        self._package_id = package_id
        self._carrier = carrier

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
    def carrier(self):
        return self._carrier

    @carrier.setter
    def carrier(self, new_carrier):
        self._carrier = new_carrier

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
        truck_manager_id: str = None,
        truck_id: str = None,
    ):
        self._truck_type = truck_type
        self._truck_length = truck_length
        self._axles = axles
        self._owner = truck_manager_id
        self._truck_id = truck_id
        self._packages: Set[Package] = set()

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
    def owner(self, user_id: str):
        self.owner = user_id

    @property
    def packages(self) -> List[Package]:
        return self._packages
    
    @packages.setter
    def packages(self, packages: List[Package]):
        self._packages = packages

    def has_packages(self):
        return len(self._packages) > 0

    def assign_package(self, package):
        if self._can_assign_package(package):
            self._packages.add(package)

    def _can_assign_package(self, package):
        return package not in self._packages

    def unassign_package(self, package):
        if package in self._packages:
            self._packages.remove(package)


class User:

    def __init__(self, user_id: str, trucks: List[Truck] = None):
        self._user_id = user_id
        self._trucks: Set[Truck] = trucks

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        self._user_id = user_id

    def has_assigned_trucks(self):
        return len(self._trucks) > 0

    def assign_truck(self, truck: Truck):
        if self._can_assign_truck(truck):
            self._trucks.add(truck)

    def _can_assign_truck(self, truck: Truck):
        return truck not in self._trucks

    def unassign_truck(self, truck):
        if truck in self._trucks:
            self._trucks.remove(truck)

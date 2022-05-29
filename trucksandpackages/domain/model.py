from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List

class Package:

    def __init__(self, shipping_type: str, weight: Decimal, shipping_date: date, package_id: str = None):
        self._shipping_type = shipping_type
        self._weight = weight
        self._shipping_date = shipping_date
        self._package_id = package_id

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

class Truck:

    def __init__(
        self,
        truck_type: str,
        truck_length: int,
        axles: int,
        max_weight_capacity: int,
        truck_manager_id: str = None,
        truck_id: str = None,
        packages: List[Package] = None
    ):
        self._truck_type = truck_type
        self._truck_length = truck_length
        self._axles = axles
        self._max_weight_capacity = max_weight_capacity
        self._owner = truck_manager_id
        self._truck_id = truck_id
        self._packages = packages

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
    def max_weight_capacity(self) -> int:
        return self._max_weight_capacity

    @max_weight_capacity.setter
    def max_weight_capacity(self, max_weight_capacity: int):
        self._max_weight_capacity = max_weight_capacity

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


class User:

    def __init__(self, user_id: str, trucks: List[Truck] = None):
        self._user_id = user_id
        self._trucks = trucks

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        self._user_id = user_id

    @property
    def trucks(self) -> List[Truck]:
        return self._trucks

    @trucks.setter
    def trucks(self, trucks: List[Truck]):
        self._trucks = trucks

from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Item:
    item_id: str
    name: str
    weight: Decimal


class Truck:

    def __init__(self, truck_id, owner, items: List[Item] = None):
        self._truck_id = truck_id
        self._owner = owner
        self._items = items

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
    def items(self) -> List[Item]:
        return self._items
    
    @items.setter
    def items(self, items: List[Item]):
        self._items = items


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
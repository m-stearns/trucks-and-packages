from typing import List

from trucksandpackages.services.unit_of_work import DatastoreUnitOfWork
from trucksandpackages.domain import model

def create_truck_manager(auth_id: str, unit_of_work: DatastoreUnitOfWork):
    with unit_of_work:
        new_user = model.User(auth_id=auth_id)
        unit_of_work.users.add(new_user)
        unit_of_work.commit()
        user_id = unit_of_work.users.id_of_added_entity
        return user_id


def get_all_truck_managers(unit_of_work: DatastoreUnitOfWork) -> List[model.User]:
    with unit_of_work:
        truck_managers = unit_of_work.users.get_list()
        return truck_managers

def create_truck(
    type: str,
    length: int,
    axles: int,
    owner: str,
    unit_of_work: DatastoreUnitOfWork
) -> str:
    with unit_of_work:
        new_truck = model.Truck(
            type, length, axles, truck_manager_id=owner
        )
        unit_of_work.trucks.add(new_truck)
        unit_of_work.commit()
        truck_id = unit_of_work.trucks.id_of_added_entity
        return truck_id

def get_truck(truck_id: str, unit_of_work: DatastoreUnitOfWork) -> model.Truck:
    with unit_of_work:
        truck = unit_of_work.trucks.get(truck_id)
        if truck:
            return truck
        else:
            return None
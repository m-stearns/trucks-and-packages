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

def get_truck_manager_by_auth_id(
    auth_id: str,
    unit_of_work: DatastoreUnitOfWork
) -> model.User:
    with unit_of_work:
        users = unit_of_work.users.get_list()
        for user in users:
            if user.auth_id == auth_id:
                return user
        return None

def create_truck(
    type: str,
    length: int,
    axles: int,
    auth_id: str,
    unit_of_work: DatastoreUnitOfWork
) -> str:
    with unit_of_work:
        new_truck = model.Truck(
            type, length, axles, owner=auth_id
        )
        unit_of_work.trucks.add(new_truck)
        unit_of_work.commit()
        truck_id = unit_of_work.trucks.id_of_added_entity
        return truck_id

def get_truck(truck_id: str, unit_of_work: DatastoreUnitOfWork) -> model.Truck:
    with unit_of_work:
        truck = unit_of_work.trucks.get(truck_id)
        if truck:
            if truck.has_packages():
                pass
            return truck
        else:
            return None

def edit_truck(
    truck: model.Truck,
    truck_type: str,
    truck_length: int,
    axles: int,
    unit_of_work: DatastoreUnitOfWork,
    clear_package_ids: bool = False,
):
    with unit_of_work:
        truck.truck_type = truck_type if truck_type else truck.truck_type
        truck.truck_length = truck_length if truck_length else truck.truck_length
        truck.axles = axles if axles else truck.axles
        if clear_package_ids:
            truck.package_ids = set()
        unit_of_work.trucks.add(truck)
        unit_of_work.commit()

def delete_truck(
    truck_id: str,
    unit_of_work: DatastoreUnitOfWork
):
    with unit_of_work:
        unit_of_work.trucks.remove(truck_id)
        unit_of_work.commit()
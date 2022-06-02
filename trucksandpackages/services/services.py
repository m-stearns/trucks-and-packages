from datetime import date
from decimal import Decimal
from typing import List

from trucksandpackages.domain import model
from trucksandpackages.services.unit_of_work import DatastoreUnitOfWork


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
            return truck
        else:
            return None

def edit_truck(
    truck: model.Truck,
    unit_of_work: DatastoreUnitOfWork,
    truck_type: str = None,
    truck_length: int = None,
    axles: int = None,
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

def get_trucks(
    query_limit: int,
    query_offset: str,
    unit_of_work: DatastoreUnitOfWork
):
    with unit_of_work:
        trucks, next_page_available = unit_of_work.trucks.get_list(
            query_limit, query_offset
        )
        return (trucks, next_page_available)

def create_package(
    shipping_type: str,
    weight: Decimal,
    shipping_date: date,
    unit_of_work: DatastoreUnitOfWork
) -> str:
    with unit_of_work:
        new_package = model.Package(
            shipping_type, weight, shipping_date, carrier_id=None
        )
        unit_of_work.packages.add(new_package)
        unit_of_work.commit()
        package_id = unit_of_work.packages.id_of_added_entity
        return package_id

def get_packages(
    query_limit: int,
    query_offset: str,
    unit_of_work: DatastoreUnitOfWork
):
    with unit_of_work:
        packages, next_page_available = unit_of_work.packages.get_list(
            query_limit, query_offset
        )
        return (packages, next_page_available)

def get_package(package_id: str, unit_of_work: DatastoreUnitOfWork) -> model.Package:
    with unit_of_work:
        package = unit_of_work.packages.get(package_id)
        if package:
            return package
        else:
            return None

def edit_package(
    package: model.Package,
    unit_of_work: DatastoreUnitOfWork,
    shipping_type: str = None,
    weight: Decimal = None,
    shipping_date: date = None,
    clear_carrier: bool = False,
):
    with unit_of_work:
        package.shipping_type = shipping_type if shipping_type else package.shipping_type
        package.weight = weight if weight else package.weight
        package.shipping_date = shipping_date if shipping_date else package.shipping_date
        if clear_carrier:
            package.carrier_id = None
        unit_of_work.packages.add(package)
        unit_of_work.commit()

def delete_package(
    package_id: str,
    unit_of_work: DatastoreUnitOfWork
):
    with unit_of_work:
        unit_of_work.packages.remove(package_id)
        unit_of_work.commit()
        if unit_of_work.packages.id_of_deleted_entity:
            return True
        else:
            return False
from typing import List

from google.cloud import datastore
from trucksandpackages.domain import model
from trucksandpackages.repositories.abstract_repository import AbstractRepository

class TruckRepository(AbstractRepository):

    def __init__(
        self,
        client_session: datastore.Client,
        datastore_config: datastore,
        transaction: datastore.Transaction
    ):
        self._client_session = client_session
        self._datastore = datastore_config
        self._transaction = transaction
        self._added_entity: datastore.Entity = None
        self._id_of_deleted_entity: str = None

    @property
    def id_of_added_entity(self) -> str:
        return self._added_entity.key.id

    @property
    def id_of_deleted_entity(self) -> str:
        return self._id_of_deleted_entity

    def add(self, truck: model.Truck):
        if truck.truck_id:
            key = self._client_session.key("trucks", int(truck.truck_id))
        else:
            key = self._client_session.key("trucks")

        entity = self._datastore.Entity(key=key)
        entity.update({
            "type": truck.truck_type,
            "length": truck.truck_length,
            "axles": truck.axles,
            "owner": truck.owner,
            "packages": [],
        })
        self._transaction.put(entity)
        self._added_entity = entity


    def get(self, truck_id: str):
        
        key = self._client_session.key("trucks", int(truck_id))
        result = self._client_session.get(key=key)
        if result:
            truck = model.Truck(
                truck_type=result["type"],
                truck_length=result["length"],
                axles=result["axles"],
                truck_manager_id=result["owner"],
                truck_id=result.key.id
            )
            for package_id in result["packages"]:
                package = self.__get_package_by_id(package_id)
                package.carrier = truck
                truck.assign_package(package)
            return truck
        else:
            return None

    def get_list(self):
        pass

    def remove(self):
        pass

    def __get_package_by_id(self, package_id: str) -> model.Package:
        key = self.client_session.key("packages", int(package_id))
        result = self.client_session.get(key=key)
        if result:
            package = model.Package(
                shipping_type=result["shipping_type"],
                weight=result["weight"],
                shipping_date=result["shipping_date"],
                package_id=result.key.id
            )
            return package
        return None
        

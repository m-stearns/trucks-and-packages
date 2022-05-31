from typing import List
from google.cloud import datastore

from trucksandpackages.domain.model import Truck

class TruckRepository:

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

    def add(self, truck: Truck):
        if truck.truck_id:
            key = self._client_session.key("trucks", int(truck.truck_id))
        else:
            key = self._client_session.key("trucks")

        entity = self._datastore.Entity(key=key)
        entity.update({
            "type": truck.truck_type,
            "length": truck.truck_length,
            "axles": truck.axles,
            "owner": truck.owner
        })
        self._transaction.put(entity)
        self._added_entity = entity
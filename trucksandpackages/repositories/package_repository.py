from typing import List, Tuple

from google.cloud import datastore
from trucksandpackages.domain import model
from trucksandpackages.repositories.abstract_repository import AbstractRepository

class PackageRepository(AbstractRepository):

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

    def add(self, package: model.Package):
        if package.package_id:
            key = self._client_session.key("packages", int(package.package_id))
        else:
            key = self._client_session.key("packages")

        entity = self._datastore.Entity(key=key)
        entity.update({
            "shipping_type": package.shipping_type,
            "weight": str(package.weight),
            "shipping_date": str(package.shipping_date),
            "carrier": package.carrier_id,
        })
        self._transaction.put(entity)
        self._added_entity = entity


    def get(self, package_id: str):
        key = self._client_session.key("packages", int(package_id))
        result = self._client_session.get(key=key)
        if result:
            package = model.Package(
                shipping_type=result["shipping_type"],
                weight=result["weight"],
                shipping_date=result["shipping_date"],
                carrier_id=result["carrier"],
                package_id=result.key.id
            )
            return package
        else:
            return None

    def get_list(self, limit: int, offset: int) -> Tuple[List[model.Package], bool]:
        query = self._client_session.query(kind="packages")
        query_iterator = query.fetch(limit=limit, offset=offset)
        pages = query_iterator.pages
        results = list(next(pages))
        packages = []
        for item in results:
            packages.append(
                model.Package(
                    shipping_type=item["shipping_type"],
                    weight=item["weight"],
                    shipping_date=item["shipping_date"],
                    carrier_id=item["carrier"],
                    package_id=item.key.id
                )
            )

        if query_iterator.next_page_token:
            next_page_available = True
        else:
            next_page_available = False
        return (packages, next_page_available)

    def remove(self, package_id: str):
        package_key = self._client_session.key("packages", int(package_id))
        result = self._client_session.get(key=package_key)
        if result:
            self._transaction.delete(package_key)
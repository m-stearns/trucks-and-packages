from google.cloud import datastore

from trucksandpackages.repositories.truck_repository import TruckRepository
from trucksandpackages.repositories.user_repository import UserRepository

class DatastoreUnitOfWork:

    def __init__(self):
        self.datastore = datastore

    def __enter__(self):
        self.client_session = datastore.Client()
        self.transaction = self.client_session.transaction()
        self.transaction.begin()
        self.users = UserRepository(
            self.client_session,
            self.datastore,
            self.transaction
        )
        self.trucks = TruckRepository(
            self.client_session,
            self.datastore,
            self.transaction
        )

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self.transaction.commit()

    def rollback(self):
        if self.transaction._status == self.transaction._IN_PROGRESS:
            self.transaction.rollback()
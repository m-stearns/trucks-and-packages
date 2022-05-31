from trucksandpackages.services.unit_of_work import DatastoreUnitOfWork
from trucksandpackages.domain import model

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
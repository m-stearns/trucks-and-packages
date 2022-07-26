from trucksandpackages.domain.model import Truck, User

def test_assign_truck_to_user():
    truck = Truck("Box truck", 20, 2, "abc123", "7251")
    user = User("abc123")
    user.assign_truck(truck.truck_id)

    assert user.has_assigned_trucks()
    assert len(user.truck_ids) == 1
    assert truck.truck_id in user.truck_ids

def test_assign_truck_is_idempotent():
    truck = Truck("Box truck", 20, 2, "abc123", "7251")
    user = User("abc123")
    user.assign_truck(truck.truck_id)
    user.assign_truck(truck.truck_id)

    assert len(user.truck_ids) == 1

def test_unassign_truck_from_user():
    truck = Truck("Box truck", 20, 2, "abc123", "7251")
    user = User("abc123")
    user.truck_ids.add(truck.truck_id)

    user.unassign_truck(truck.truck_id)

    assert len(user.truck_ids) == 0
    assert truck.truck_id not in user.truck_ids
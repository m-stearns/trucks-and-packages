from decimal import Decimal
from trucksandpackages.domain.model import Truck, Package

def test_assign_package_to_a_truck():
    truck = Truck("Box truck", 20, 2, "abc123")
    package = Package("overnight", Decimal(5.0), "06/25/2022", "938xyz")
    truck.assign_package_id(package.package_id)

    assert truck.has_packages()
    assert len(truck.package_ids) == 1
    assert "938xyz" in truck.package_ids

def test_assign_package_is_idempotent():
    truck = Truck("Box truck", 20, 2, "abc123")
    package = Package("overnight", Decimal(5.0), "06/25/2022", "938xyz")
    truck.assign_package_id(package.package_id)
    truck.assign_package_id(package.package_id)

    assert len(truck.package_ids) == 1

def test_unassign_package_from_truck():
    truck = Truck("Box truck", 20, 2, "abc123")
    package = Package("overnight", Decimal(5.0), "06/25/2022", "938xyz")
    truck.package_ids.add(package.package_id)

    truck.unassign_package_id(package.package_id)

    assert len(truck.package_ids) == 0
    assert package.package_id not in truck.package_ids
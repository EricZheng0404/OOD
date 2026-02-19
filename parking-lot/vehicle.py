"""
[DONE]
Vehicle class and its subclasses.
"""
from enum import Enum

class VehicleSize(Enum):
    """
    VehicleSize.SMALL.name gives us the string "SMALL", 
    VehicleSize.SMALL.value gives us the value 1.
    """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleSize):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

    @property
    def vehicle_size(self):
        return self.vehicle_type.value

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleSize.SMALL)

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleSize.MEDIUM)


class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleSize.LARGE)



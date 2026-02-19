"""
[DONE]
Parking spot class and its subclasses.
"""
from vehicle import VehicleSize, Vehicle
class ParkingSpot:
    def __init__(self, spot_id: int, spot_size: VehicleSize, vehicle=None):
        self._spot_id = spot_id
        self._spot_size = spot_size
        self._is_occupied = False
        self.parked_vehicle = vehicle

    @property
    def spot_id(self):
        return self._spot_id

    @property
    def size(self):
        return self._spot_size.value
    
    @property
    def is_occupied(self):
        return self._is_occupied
    

    def park_vehicle(self, vehicle: Vehicle):
        """Park a vehicle in this spot."""
        if self._is_occupied:
            raise Exception(f"Parking spot {self.spot_id} is already occupied.")
        if vehicle.vehicle_size > self.size:
            raise Exception(f"Vehicle size {vehicle.vehicle_size} exceeds parking spot size {self.size}.")
        self.parked_vehicle = vehicle
        self._is_occupied = True
    
    def unpark(self, vehicle: Vehicle):
        """Remove vehicle from this spot."""
        if not self.is_occupied:
            raise Exception(f"Parking spot {self.spot_id} is not occupied")
        self.parked_vehicle = None
        self._is_occupied = False

    def __repr__(self) -> str:
        status = "occupied" if not self.is_occupied else "available"
        return f"{self._spot_id}, size: {self.size}. status: {status}"
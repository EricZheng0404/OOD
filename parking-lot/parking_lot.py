from parking_manager import ParkingManager
from parking_ticket import ParkingTicket
from vehicle import Vehicle
from datetime import datetime

class ParkingLot:
    def __init__(self, spot_config):
        self.parking_manager = ParkingManager(spot_config)

    def park(self, vehicle: Vehicle) -> ParkingTicket:
        return self.parking_manager.park_vehicle(vehicle)
        
    def unpark(self, vehicle: Vehicle) -> float:
        """Unpark a vehicle and return the fare amount."""
        if vehicle not in self.parking_manager.vehicle_locations:
            raise Exception("Vehicle not found in parking lot")
        
        return self.parking_manager.unpark_vehicle(vehicle)
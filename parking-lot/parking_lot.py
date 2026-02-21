"""
Parking Lot - Main class for managing the parking lot
Supports single-level and multi-level parking.
"""
from parking_manager import ParkingManager
from parking_ticket import ParkingTicket
from vehicle import Vehicle, VehicleSize
from typing import Optional
import threading

class ParkingLot:
    def __init__(self, num_floors: int = 1, spot_config: Optional[dict[VehicleSize, int]] = None):
        """
        Initialize parking lot.
        
        :param num_floors: Number of floors (default 1)
        :param spot_config: Dictionary mapping VehicleSize to number of spots per floor
                          e.g., {VehicleSize.SMALL: 5, VehicleSize.MEDIUM: 10, VehicleSize.LARGE: 3}
        """
        self.parking_manager = ParkingManager(num_floors, spot_config)
        self._main_lock = threading.Lock()  # Main lock for thread safety

    def park(self, vehicle: Vehicle) -> ParkingTicket:
        """Park a vehicle and return a ticket."""
        with self._main_lock:   
            return self.parking_manager.park_vehicle(vehicle)
        
    def unpark(self, vehicle: Vehicle) -> float:
        """Unpark a vehicle and return the fare amount."""
        with self._main_lock:
            if vehicle not in self.parking_manager.vehicle_locations:
               raise Exception(f"Vehicle {vehicle.license_plate} not found in parking lot")
        
        return self.parking_manager.unpark_vehicle(vehicle)
    
    def get_vehicle_location(self, vehicle: Vehicle) -> dict:
        """Get the location (floor and spot) of a parked vehicle."""
        location = self.parking_manager.get_vehicle_location(vehicle)
        if not location:
            raise Exception(f"Vehicle {vehicle.license_plate} not found")
        
        floor_num, spot = location
        return {
            "floor": floor_num,
            "spot_id": spot.spot_id,
            "spot_size": spot._spot_size.name
        }
    
    def get_parking_status(self) -> dict:
        """Get overall parking lot status."""
        return {
            "total_floors": self.parking_manager.num_floors,
            "num_vehicles_parked": len(self.parking_manager.vehicle_locations),
            "available_small": self.parking_manager.get_available_spots(VehicleSize.SMALL),
            "available_medium": self.parking_manager.get_available_spots(VehicleSize.MEDIUM),
            "available_large": self.parking_manager.get_available_spots(VehicleSize.LARGE),
        }
    
    def get_floor_status(self, floor_num: int) -> dict:
        """Get status of a specific floor."""
        return self.parking_manager.get_floor_info(floor_num)
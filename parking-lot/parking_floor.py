"""
Parking Floor class - represents a single floor in a multi-level parking lot.
Each floor manages its own parking spots.
"""
from typing import Optional
from parking_spot import ParkingSpot
from vehicle import Vehicle, VehicleSize
from collections import defaultdict, deque


class ParkingFloor:
    def __init__(self, floor_num: int, spot_config: Optional[dict[VehicleSize, int]] = None):
        """
        Initialize a parking floor.
        
        :param floor_num: Floor number (0-indexed)
        :param spot_config: Dictionary mapping VehicleSize to number of spots
        """
        self.floor_num = floor_num
        # VehicleSize -> deque of ParkingSpots
        self.parking_spots = defaultdict(deque)
        # Vehicle -> ParkingSpot
        self.vehicle_locations: dict[Vehicle, ParkingSpot] = {}
        self._size = self.get_total_spots(spot_config)
        if spot_config:
            self._initialize_spots(spot_config)
    
    def get_total_spots(self, spot_config: Optional[dict[VehicleSize, int]]) -> int:
        """Calculate total number of spots based on the spot configuration."""
        if not spot_config:
            return 0
        return sum(spot_config.values())
    
    @property
    def size(self) -> int:
        """Get total number of spots on this floor."""
        return self._size
    
    def _initialize_spots(self, spot_config):
        """Initialize parking spots for this floor."""
        spot_id = 1
        for vehicle_size, amount in spot_config.items():
            for _ in range(amount):
                # Spot ID is unique per floor: floor_num * 1000 + spot_id
                spot_id_global = self.floor_num * 1000 + spot_id
                new_spot = ParkingSpot(spot_id_global, vehicle_size)
                self.parking_spots[vehicle_size].append(new_spot)
                spot_id += 1
    
    def find_empty_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        Find an empty spot for the vehicle.
        Prioritizes smallest available spot.
        """
        for size in [VehicleSize.SMALL, VehicleSize.MEDIUM, VehicleSize.LARGE]:
            if size.value >= vehicle.vehicle_size and self.parking_spots[size]:
                return self.parking_spots[size].popleft()
        return None
    
    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Park a vehicle on this floor."""
        parking_spot = self.find_empty_spot(vehicle)
        if not parking_spot:
            return None
        
        parking_spot.park_vehicle(vehicle)
        self.vehicle_locations[vehicle] = parking_spot
        return parking_spot
    
    def unpark_vehicle(self, vehicle: Vehicle) -> ParkingSpot:
        """Unpark a vehicle from this floor."""
        if vehicle not in self.vehicle_locations:
            raise Exception(f"Vehicle {vehicle.license_plate} not found on floor {self.floor_num}")
        
        parking_spot = self.vehicle_locations[vehicle]
        parking_spot.unpark(vehicle)
        del self.vehicle_locations[vehicle]
        # Return the spot to the pool
        self.parking_spots[parking_spot._spot_size].append(parking_spot)
        return parking_spot
    
    def is_full(self) -> bool:
        """Check if this floor has any available spots."""
        for spots in self.parking_spots.values():
            if spots:
                return False
        return True
    
    def get_available_spots(self, vehicle_size: VehicleSize) -> int:
        """Get count of available spots for a vehicle size."""
        return len(self.parking_spots[vehicle_size])
    
    def get_occupancy(self) -> float:
        """Get occupancy rate as a percentage."""
        total_spots = sum(len(spots) for spots in self.parking_spots.values())
        total_spotted = sum(len(spots) for spots in self.parking_spots.values())
        if total_spots == 0:
            return 0.0
        return (total_spots - total_spotted) / total_spots * 100

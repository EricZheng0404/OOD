"""
Parking Manager - Manages single or multi-level parking
"""
from typing import Optional
from parking_spot import ParkingSpot
from parking_floor import ParkingFloor
from vehicle import Vehicle, VehicleSize
from parking_ticket import FlatRate, ParkingTicket
import time


class ParkingManager:
    def __init__(self, num_floors: int = 1, spot_config: Optional[dict[VehicleSize, int]] = None):
        """
        Initialize parking manager.
        
        :param num_floors: Number of floors in the parking lot
        :param spot_config: Dictionary mapping VehicleSize to number of spots per floor
        """
        self.num_floors = num_floors
        self.floors: list[ParkingFloor] = []
        
        # Vehicle -> (floor_num, ParkingSpot)
        self.vehicle_locations: dict[Vehicle, tuple[int, ParkingSpot]] = {}
        # Ticket system: vehicle -> ticket
        self.tickets: dict[Vehicle, ParkingTicket] = {}
        
        # Initialize floors
        for floor_num in range(num_floors):
            floor = ParkingFloor(floor_num, spot_config)
            self.floors.append(floor)
    
    def find_empty_spot(self, vehicle: Vehicle) -> Optional[tuple[int, ParkingSpot]]:
        """
        Find an empty spot across all floors.
        Returns (floor_num, spot) or None.
        Tries floors in order: closest floor first.
        """
        for floor in self.floors:
            spot = floor.find_empty_spot(vehicle)
            if spot:
                return (floor.floor_num, spot)
        return None
    
    def park_vehicle(self, vehicle: Vehicle):
        """Park a vehicle and generate a ticket."""
        result = self.find_empty_spot(vehicle)
        if not result:
            raise Exception("No available spot in any floor")
        
        floor_num, parking_spot = result
        floor = self.floors[floor_num]
        
        # Park on the floor
        parking_spot.park_vehicle(vehicle)
        
        # Track location
        self.vehicle_locations[vehicle] = (floor_num, parking_spot)
        
        # Create ticket
        ticket = ParkingTicket(vehicle, time.time(), FlatRate(5.0))
        self.tickets[vehicle] = ticket
        
        return ticket
    
    def unpark_vehicle(self, vehicle: Vehicle) -> float:
        """Unpark a vehicle and return the fare."""
        if vehicle not in self.vehicle_locations:
            raise Exception(f"Vehicle {vehicle.license_plate} not found")
        
        floor_num, parking_spot = self.vehicle_locations[vehicle]
        floor = self.floors[floor_num]
        
        # Unpark from floor
        parking_spot.unpark(vehicle)
        
        # Return spot to pool
        floor.parking_spots[parking_spot._spot_size].append(parking_spot)
        
        # Clean up tracking
        del self.vehicle_locations[vehicle]
        ticket = self.tickets[vehicle]
        del self.tickets[vehicle]
        
        return ticket.calculate_ticket_fare()
    
    def get_vehicle_location(self, vehicle: Vehicle) -> Optional[tuple[int, ParkingSpot]]:
        """Get the floor and spot where a vehicle is parked."""
        return self.vehicle_locations.get(vehicle)
    
    def get_available_spots(self, vehicle_size: VehicleSize) -> int:
        """Get total available spots across all floors."""
        total = 0
        for floor in self.floors:
            total += floor.get_available_spots(vehicle_size)
        return total
    
    def get_occupancy_rate(self) -> float:
        """Get overall occupancy rate of the parking lot."""
        total_parked = len(self.vehicle_locations)
        total_spots = sum(floor.size for floor in self.floors)
        return (total_parked / total_spots) * 100
    
    def get_floor_info(self, floor_num: int) -> dict:
        """Get info about a specific floor."""
        if floor_num >= len(self.floors):
            raise Exception(f"Floor {floor_num} does not exist")
        
        floor = self.floors[floor_num]
        return {
            "floor": floor_num,
            "available_small": floor.get_available_spots(VehicleSize.SMALL),
            "available_medium": floor.get_available_spots(VehicleSize.MEDIUM),
            "available_large": floor.get_available_spots(VehicleSize.LARGE),
        }
    

        
    





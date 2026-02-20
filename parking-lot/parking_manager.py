"""
Parking Manager clas
"""
from typing import Optional
from parking_spot import ParkingSpot
from vehicle import Vehicle, VehicleSize
from parking_ticket import FlatRate, ParkingTicket
from collections import defaultdict, deque
import time

class ParkingManager:
    def __init__(self, spot_config: Optional[dict[VehicleSize, int]] = None):
        # VehicleSize -> [ParkingSpot]
        self.parking_spots = defaultdict(deque)
        # Vehicle -> ParkingSpot
        self.vehicle_locations: dict[Vehicle, ParkingSpot] = {}
        # Ticket system: vehicle -> ticket
        self.tickets: dict[Vehicle, ParkingTicket] = {}
        # Initilize self.parking_spots
        if spot_config:
            self._initialize_spots(spot_config)
        
    def _initialize_spots(self, spot_config):
        spot_id = 1
        for vehicle_size, amount in spot_config.items():
            for _ in range(amount):
                new_spot = ParkingSpot(spot_id, vehicle_size)
                self.parking_spots[vehicle_size].append(new_spot)
                spot_id += 1

    def find_empty_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        # Check in order: SMALL, MEDIUM, LARGE
        # We always start from the smallest spot
        for size in [VehicleSize.SMALL, VehicleSize.MEDIUM, VehicleSize.LARGE]:
            if size.value >= vehicle.vehicle_size and self.parking_spots[size]:
                return self.parking_spots[size].popleft()
        return None
    
    def park_vehicle(self, vehicle: Vehicle):
        """
        Docstring for park_vehicle
        
        :param self: Description
        :param vehicle: Description
        :type vehicle: Vehicle
        """
        parking_spot = self.find_empty_spot(vehicle)
        if not parking_spot:
            raise Exception("No available spot")
        is_occupied = parking_spot._is_occupied
        if is_occupied:
            raise Exception("The spot already occupied")
        parking_spot.park_vehicle(vehicle)
        self.vehicle_locations[vehicle] = parking_spot
        ticket = ParkingTicket(vehicle, time.time(), FlatRate(5.0))
        self.tickets[vehicle] = ticket
        return ticket

    def unpark_vehicle(self, vehicle: Vehicle) -> float:
        parking_spot = self.vehicle_locations[vehicle]
        parking_spot.unpark(vehicle)
        del self.vehicle_locations[vehicle]
        ticket = self.tickets[vehicle]
        del self.tickets[vehicle]
        return ticket.calculate_ticket_fare()
    
    def get_available_spots(self, vehicle_size: VehicleSize) -> int:
        return len(self.parking_spots[vehicle_size])
    

        
    





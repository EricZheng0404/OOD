"""
Parking Manager clas
"""
from typing import Optional
from parking_spot import ParkingSpot
from vehicle import Vehicle, VehicleSize
from parking_ticket import ParkingTicket
from collections import defaultdict, deque
from datetime import datetime
from parking_ticket import ParkingTicket

class ParkingManager:
    def __init__(self, spot_config: Optional[dict[VehicleSize, int]] = None):
        # VehicleS -> [ParkingSpot]
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
        if not is_occupied:
            raise Exception("The spot already occupied")
        parking_spot._is_occupied = True
        parking_spot.parked_vehicle = vehicle
        self.vehicle_locations[vehicle] = parking_spot
        ticket = ParkingTicket(vehicle, datetime.now())
        self.tickets[vehicle] = ticket
        return ticket

    
    def unpark_vehicle(self, vehicle: Vehicle) -> float:
        parking_spot = self.vehicle_locations[vehicle]
        parking_spot._is_occupied = False
        parking_spot.parked_vehicle = None
        del self.vehicle_locations[vehicle]
        ticket = self.tickets[vehicle]
        del self.tickets[vehicle]
        return ticket.calculate_fare()
        
    





"""
Parking Ticket System

Notes:
1. Used a constant dictionary for quick lookup of hourly_rates.
2. Should use self for class constants.

"""
from vehicle import Vehicle
from datetime import datetime

class ParkingTicket:
    # Hourly rates per vehicle size (SMALL=1, MEDIUM=2, LARGE=3)
    HOURLY_RATES = {
        1: 2,    # Small
        2: 3,    # Medium
        3: 5     # Large
    }
    
    def __init__(self, vehicle: Vehicle, start_time: datetime):
        self.vehicle = vehicle
        self.start_time = start_time

    def calculate_fare(self):
        duration = datetime.now() - self.start_time
        parking_hours = duration.total_seconds() / 3600
        rate = self.HOURLY_RATES[self.vehicle.vehicle_size]
        return parking_hours * rate
    

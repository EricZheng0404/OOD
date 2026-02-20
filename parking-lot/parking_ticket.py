"""
Parking Ticket System

Notes:
1. Used a constant dictionary for quick lookup of hourly_rates.
2. Should use self for class constants.

"""
from vehicle import Vehicle
import time
from abc import ABC, abstractmethod

# Strategy pattern
# This is an abstract class
class RateStrategy:
    @abstractmethod
    def calculate_fare(self, vehicle: Vehicle, duration: float) -> float:
        pass

class HourlyPricingRate(RateStrategy):
    def __init__(self, hourly_rates: dict[int, float]):
        self.hourly_rates = hourly_rates

    def calculate_fare(self, vehicle: Vehicle, duration: float) -> float:
        vehicle_size = vehicle.vehicle_size
        rate = self.hourly_rates.get(vehicle_size)
        if rate is None:
            raise ValueError("Invalid vehicle size")
        return duration * rate

class FlatRate(RateStrategy):
    def __init__(self, flat_rate: float):
        self.flat_rate = flat_rate

    def calculate_fare(self, vehicle: Vehicle, duration: float) -> float:
        return self.flat_rate
    

class ParkingTicket:
    def __init__(self, vehicle: Vehicle, start_time: float, rate_strategy: RateStrategy):
        self.vehicle = vehicle
        self.start_time = start_time
        # Strategy pattern in here, giving users flexibility to choose different rate strategies
        self.rate_strategy = rate_strategy

    def calculate_ticket_fare(self):
        duration = time.time() - self.start_time
        parking_hours = duration / 3600
        return self.rate_strategy.calculate_fare(self.vehicle, parking_hours)


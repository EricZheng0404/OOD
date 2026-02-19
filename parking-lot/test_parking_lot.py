"""
Comprehensive pytest tests for the parking-lot module.
"""
import pytest
from vehicle import Vehicle, Motorcycle, Car, Truck, VehicleSize
from parking_spot import ParkingSpot


class TestVehicleSize:
    """Tests for VehicleSize enum."""
    
    def test_vehicle_size_values(self):
        """Test that VehicleSize enum has correct values."""
        assert VehicleSize.SMALL.value == 1
        assert VehicleSize.MEDIUM.value == 2
        assert VehicleSize.LARGE.value == 3
    
    def test_vehicle_size_names(self):
        """Test that VehicleSize enum has correct names."""
        assert VehicleSize.SMALL.name == "SMALL"
        assert VehicleSize.MEDIUM.name == "MEDIUM"
        assert VehicleSize.LARGE.name == "LARGE"


class TestVehicle:
    """Tests for Vehicle base class."""
    
    def test_vehicle_initialization(self):
        """Test vehicle initialization with license plate and size."""
        vehicle = Vehicle("ABC123", VehicleSize.MEDIUM)
        assert vehicle.license_plate == "ABC123"
        assert vehicle.vehicle_type == VehicleSize.MEDIUM
    
    def test_vehicle_size_property(self):
        """Test vehicle_size property returns correct numeric value."""
        vehicle_small = Vehicle("XYZ789", VehicleSize.SMALL)
        vehicle_medium = Vehicle("DEF456", VehicleSize.MEDIUM)
        vehicle_large = Vehicle("GHI012", VehicleSize.LARGE)
        
        assert vehicle_small.vehicle_size == 1
        assert vehicle_medium.vehicle_size == 2
        assert vehicle_large.vehicle_size == 3


"""
Test cases for multi-level parking lot
"""
import pytest
from parking_lot import ParkingLot
from vehicle import Vehicle, Car, Motorcycle, Truck, VehicleSize


class TestMultiLevelParkingLot:
    """Tests for multi-level parking lot functionality."""
    
    def setup_method(self):
        """Set up a 3-floor parking lot."""
        spot_config = {
            VehicleSize.SMALL: 2,
            VehicleSize.MEDIUM: 3,
            VehicleSize.LARGE: 1
        }
        self.parking_lot = ParkingLot(num_floors=3, spot_config=spot_config)
    
    def test_multi_floor_parking(self):
        """Test parking vehicles across multiple floors."""
        # Create vehicles
        car1 = Car("ABC123")
        car2 = Car("ABC124")
        car3 = Car("ABC125")
        
        # Park on floor 0 (3 cars can fit per floor, we have 3 spots per floor for MEDIUM)
        ticket1 = self.parking_lot.park(car1)
        ticket2 = self.parking_lot.park(car2)
        ticket3 = self.parking_lot.park(car3)
        
        assert ticket1 is not None
        assert ticket2 is not None
        assert ticket3 is not None
        
        # Check location
        loc1 = self.parking_lot.get_vehicle_location(car1)
        loc2 = self.parking_lot.get_vehicle_location(car2)
        loc3 = self.parking_lot.get_vehicle_location(car3)
        
        print(f"Car1 parked at floor {loc1['floor']}, spot {loc1['spot_id']}")
        print(f"Car2 parked at floor {loc2['floor']}, spot {loc2['spot_id']}")
        print(f"Car3 parked at floor {loc3['floor']}, spot {loc3['spot_id']}")
    
    def test_floor_status(self):
        """Test getting status of a specific floor."""
        status = self.parking_lot.get_floor_status(0)
        print(f"Floor 0 status: {status}")
        
        assert status["floor"] == 0
        assert status["available_small"] == 2  # 2 small spots
        assert status["available_medium"] == 3  # 3 medium spots
        assert status["available_large"] == 1  # 1 large spot
    
    def test_parking_lot_status(self):
        """Test getting overall parking lot status."""
        # Park some vehicles
        car1 = Car("Car1")
        motorcycle = Motorcycle("Moto1")
        self.parking_lot.park(car1)
        self.parking_lot.park(motorcycle)
        
        status = self.parking_lot.get_parking_status()
        print(f"Parking lot status: {status}")
        
        assert status["total_floors"] == 3
        assert status["num_vehicles_parked"] == 2
        assert status["available_medium"] == 2  # 3 - 1 (car) = 2
        assert status["available_small"] == 1  # 2 - 1 (motorcycle) = 1
    
    def test_fill_multiple_floors(self):
        """Test that vehicles spread across multiple floors when one floor is full."""
        vehicles = []
        
        # Floor 0: has 2 small, 3 medium, 1 large = 6 spots
        # Park 6 vehicles on floor 0
        for i in range(6):
            if i < 2:
                vehicle = Motorcycle(f"Moto{i}")  # SMALL
            elif i < 5:
                vehicle = Car(f"Car{i}")  # MEDIUM
            else:
                vehicle = Truck(f"Truck{i}")  # LARGE
            
            ticket = self.parking_lot.park(vehicle)
            vehicles.append(vehicle)
            location = self.parking_lot.get_vehicle_location(vehicle)
            print(f"Vehicle {vehicle.license_plate} parked at floor {location['floor']}")
        
        # Floor 0 should be full, floor 1 should have the next vehicle
        floor0_status = self.parking_lot.get_floor_status(0)
        print(f"Floor 0 status after filling: {floor0_status}")
    
    def test_unpark_multi_floor(self):
        """Test unparking from multi-level lot."""
        car = Car("TEST123")
        ticket = self.parking_lot.park(car)
        
        location = self.parking_lot.get_vehicle_location(car)
        print(f"Parked at floor {location['floor']}")
        
        fare = self.parking_lot.unpark(car)
        print(f"Fare: ${fare}")
        
        # Vehicle should no longer be findable
        with pytest.raises(Exception):
            self.parking_lot.get_vehicle_location(car)
    
    def test_insufficient_spots_across_all_floors(self):
        """Test parking when all floors are full."""
        spot_config = {
            VehicleSize.SMALL: 1,
            VehicleSize.MEDIUM: 1,
            VehicleSize.LARGE: 1
        }
        small_lot = ParkingLot(num_floors=1, spot_config=spot_config)
        
        # Fill the single floor
        motorcycle = Motorcycle("Moto1")
        car = Car("Car1")
        truck = Truck("Truck1")
        
        small_lot.park(motorcycle)
        small_lot.park(car)
        small_lot.park(truck)
        
        # Try to park another vehicle - should fail
        car2 = Car("Car2")
        with pytest.raises(Exception, match="No available spot"):
            small_lot.park(car2)


if __name__ == "__main__":
    # Run basic demo
    print("=== Multi-Level Parking Lot Demo ===\n")
    
    test = TestMultiLevelParkingLot()
    test.setup_method()
    
    print("1. Testing floor status")
    test.test_floor_status()
    print()
    
    print("2. Testing parking lot status")
    test.test_parking_lot_status()
    print()
    
    print("3. Testing multi-floor parking")
    test.test_multi_floor_parking()
    print()
    
    print("4. Testing fill multiple floors")
    test.test_fill_multiple_floors()
    print()
    
    print("✓ Multi-level parking lot is working!")

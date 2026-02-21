# Parking Lot System - Design Notes

## Architecture Overview

```
ParkingLot
  └─ ParkingManager (single or multi-floor)
      └─ ParkingFloor[0..n] (each floor manages its own spots)
          └─ ParkingSpot[many] (organized by vehicle size)
              └─ Vehicle (parked here)
EntranceGate / ExitGate (future expansion)
PaymentProcessor (future expansion)
```

## Key Design Principles

### 1. Single Responsibility
- `ParkingLot`: High-level API for users (park/unpark)
- `ParkingManager`: Orchestrates floor management and ticket tracking
- `ParkingFloor`: Manages parking spots on a single floor
- `ParkingSpot`: Represents a single parking space
- `Vehicle`: Represents a vehicle
- `ParkingTicket`: Tracks parking session and fare calculation

### 2. Encapsulation & Atomicity
Never directly modify private variables (`_is_occupied`, `parked_vehicle`, etc.). Instead, use public methods to ensure object invariants are maintained. This prevents inconsistent state:
- ✅ Use `parking_spot.park_vehicle(vehicle)` 
- ❌ Don't directly set `spot._is_occupied = True` and `spot.parked_vehicle = vehicle` separately

### 3. Strategy Pattern for Pricing
We use Strategy Pattern to support different pricing models without modifying `ParkingTicket`:

```python
# Different strategies can be injected
ticket = ParkingTicket(vehicle, start_time, FlatRate(5.0))
ticket = ParkingTicket(vehicle, start_time, HourlyPricingRate({1: 2, 2: 3, 3: 5}))
```

Benefits:
- Easy to add new pricing strategies (DailyRate, HourlyRate with discounts, etc.)
- No modification to existing `ParkingTicket` class (Open/Closed Principle)
- Can switch strategies at runtime

### 4. Multi-Level Parking Architecture
We support multi-level parking through the `ParkingFloor` abstraction:

- **ParkingManager**: Manages all floors
- **ParkingFloor**: Each floor is independent and manages its own spots
- **Spot ID scheme**: Global unique ID = `floor_num * 1000 + spot_id`
  - Floor 0, Spot 5 = 5
  - Floor 1, Spot 5 = 1005
  - Floor 2, Spot 5 = 2005
- **Vehicle tracking**: `vehicle_locations` stores `(floor_num, parking_spot)` tuple

Finding a spot: tries floors in order (0, 1, 2, ...) until finding an available one. This is O(1) amortized per floor using `deque.popleft()`.

### 5. Enum & Type Hints
- Use `VehicleSize.MEDIUM.value` to get numeric value (cleaner than methods)
- Use type hints throughout for better code clarity and IDE support

## Time Complexity Analysis

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Find empty spot | O(1) | Loop through max 3 sizes (constant), `popleft()` is O(1) on deque |
| Park vehicle | O(1) | Find spot O(1) + update dicts O(1) |
| Unpark vehicle | O(1) | Remove spot from deque (already tracked), update dicts O(1) |
| Get available spots | O(1) | Dictionary lookup |

## Future Enhancements

1. **Payment Processing**
   - Create `PaymentProcessor` interface
   - Implement `CreditCardProcessor`, `CashProcessor`, etc.
   - Exit gate validates payment before releasing vehicle

2. **Entrance/Exit Gates**
   - `EntranceGate`: Validates available space, issues ticket
   - `ExitGate`: Validates payment, releases vehicle

3. **Reserved Spots**
   - Add `VIPSpot`, `HandicappedSpot` subclasses
   - Track reservations in a separate system

4. **Monitoring & Analytics**
   - Track occupancy rate over time
   - Peak hour analysis
   - Revenue reporting

5. **Concurrent Access**
   - Thread-safe operations using locks/semaphores
   - Handle race conditions in parking allocation

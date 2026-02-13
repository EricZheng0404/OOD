# Library Management System

A comprehensive library management system demonstrating Object-Oriented Design principles in Python.

## 📚 Overview

This system simulates a real-world library with features for:
- Book catalog management with search indexes
- Member account handling
- Book lending and returns
- Reservation queue system
- Fine calculation for overdue books
- Email notifications

## 🏗️ Architecture

### Project Structure

```
library_management_system/
├── constants.py           # Enums and configuration constants
├── library.py             # Main Library class (Facade)
├── main.py                # Application entry point
├── models/
│   ├── abstract.py        # Abstract base classes (Person, BarcodeEntity)
│   ├── account.py         # Member and LibraryCard classes
│   └── book.py            # Book, BookItem, and Rack classes
└── services/
    ├── catalog.py         # Catalog service for book management
    ├── fine_service.py    # Fine calculation service
    ├── lending_service.py # Book checkout/return service
    ├── notification_service.py  # Email notification service
    └── reservation_service.py   # Book reservation queue service
```

## 🎯 OOD Principles Demonstrated

### 1. Abstraction
- `Person` and `BarcodeEntity` abstract base classes
- Common behavior extracted into reusable base classes

### 2. Encapsulation
- Each service encapsulates its own data and behavior
- Internal implementation details hidden from external classes

### 3. Inheritance
- `Member` inherits from both `Person` and `BarcodeEntity` (Multiple Inheritance)
- `BookItem` extends `BarcodeEntity` for barcode functionality

### 4. Single Responsibility Principle (SRP)
- Each service handles one specific domain:
  - `Catalog` → Book storage and search
  - `LendingService` → Checkout/return logic
  - `ReservationService` → Queue management
  - `FineService` → Fine calculations
  - `NotificationService` → User alerts

### 5. Dependency Injection
- `LendingService` receives its dependencies through constructor injection:
```python
self.lending_service = LendingService(
    reservation_service=self.reservation_service,
    notification_service=self.notification_service
)
```

## 📊 Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              LIBRARY (Facade)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  - catalog: Catalog                                                      │
│  - lending_service: LendingService                                       │
│  - reservation_service: ReservationService                               │
│  - notification_service: NotificationService                             │
│  - members: Dict[str, Member]                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     Catalog     │       │ LendingService  │       │ReservationService│
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ books_by_isbn   │       │ active_loans    │       │ reservations    │
│ book_items      │       │ fine_service    │       ├─────────────────┤
│ titles (index)  │       ├─────────────────┤       │ make_reservation│
│ authors (index) │       │ checkout_book() │       │ get_next_reser. │
│ subjects(index) │       │ return_book()   │       │ cancel_reserv.  │
├─────────────────┤       └─────────────────┘       └─────────────────┘
│ add_book_item() │
│ search_by_title │
└─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│  BarcodeEntity  │◄──────│      Book       │
│   (Abstract)    │       │   (Metadata)    │
├─────────────────┤       ├─────────────────┤
│ barcode: str    │       │ isbn            │
└────────┬────────┘       │ title           │
         │                │ author          │
    ┌────┴────┐           │ subject         │
    │         │           │ book_item_ids   │
    ▼         ▼           └─────────────────┘
┌────────┐ ┌─────────┐
│ Member │ │BookItem │
│        │ │(Physical│
│        │ │  Copy)  │
└────────┘ └─────────┘
```

## 🔧 Key Components

### Models

| Class | Description |
|-------|-------------|
| `Person` | Abstract base class for human entities |
| `BarcodeEntity` | Mixin for entities requiring barcode scanning |
| `Member` | Library member with account and card |
| `LibraryCard` | Member's library card with unique ID |
| `Book` | Book metadata (ISBN, title, author, subject) |
| `BookItem` | Physical copy of a book on the shelf |
| `Rack` | Physical location identifier in the library |

### Services

| Service | Responsibility |
|---------|---------------|
| `Catalog` | Manages book inventory and search indexes |
| `LendingService` | Handles checkout/return with business rules |
| `ReservationService` | Manages FIFO reservation queues |
| `FineService` | Calculates overdue fines ($0.50/day) |
| `NotificationService` | Sends email notifications to members |

### Enums & Constants

```python
class AccountStatus(Enum):
    ACTIVE, CLOSED, BLACKLISTED, CANCELED

class BookStatus(Enum):
    AVAILABLE, BORROWED, RESERVED, LOST

class Constants:
    MAX_BOOKS_CHECKOUT = 5
    MAX_DAYS_CHECKOUT = 10
```

## 📖 Usage Example

```python
from library_management_system.library import Library
from library_management_system.models.account import Member
from library_management_system.models.book import Book, BookItem, Rack

# Initialize library
library = Library("Central Library", "123 Main St")

# Create a member
member = Member(barcode="M001", name="John Doe", email="john@example.com")
library.add_member(member)

# Create book and physical copy
book = Book(isbn="978-0-13-468599-1", title="Clean Code", author="Robert C. Martin", subject="Software Engineering")
rack = Rack(number=1, location_identifier="A1-Shelf-3")
book_item = BookItem(barcode="B001", book=book, rack=rack)

# Add to catalog
library.catalog.add_book_item(book_item)

# Checkout book
library.lending_service.checkout_book(member, book_item)

# Make a reservation (if book is not available)
library.reservation_service.make_reservation(member, book)

# Return book
library.lending_service.return_book(member, book_item)
```

## 📝 Design Decisions

1. **Separation of Book and BookItem**: `Book` represents metadata (can have multiple copies), while `BookItem` represents a physical copy with status and location.

2. **Service-Oriented Architecture**: Business logic is encapsulated in dedicated services rather than domain models, promoting loose coupling.

3. **Dependency Injection**: Services receive their dependencies through constructors, making the code testable and flexible.

4. **FIFO Reservation Queue**: Reservations use `deque` for efficient queue operations when multiple members want the same book.

5. **Barcode-Based Identification**: Both members and book items use barcodes for unique identification, simulating real library operations.

## 🔜 Future Improvements

- [ ] Add librarian role with different permissions
- [ ] Implement book search by author and subject
- [ ] Add database persistence layer
- [ ] Implement renewal functionality
- [ ] Add payment processing for fines

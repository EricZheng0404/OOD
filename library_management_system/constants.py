from enum import Enum

class AccountStatus(Enum):
    ACTIVE = 1
    CLOSED = 2
    BLACKLISTED = 3
    CANCELED = 4

class BookStatus(Enum):
    AVAILABLE = 1
    BORROWED = 2
    RESERVED = 3
    LOST = 4

class Constants:
    MAX_BOOKS_CHECKOUT = 5
    MAX_DAYS_CHECKOUT = 10
from datetime import datetime, timedelta
import uuid
from constants import AccountStatus
from models.abstract import Person, BarcodeEntity

class LibraryCard:
    def __init__(self):
        self.card_number = str(uuid.uuid4())
        self.issued_at = datetime.now()
        self.is_active = True

class Member(Person, BarcodeEntity):
    def __init__(self, barcode: str, name: str, email: str):
        # Explicitly calling constructors for multiple inheritance
        Person.__init__(self, name, email)
        BarcodeEntity.__init__(self, barcode)
        
        self.library_card = LibraryCard()
        self.status = AccountStatus.ACTIVE
        self.total_books_checked_out = 0 
        # Note: We rely on LendingService to track WHICH books
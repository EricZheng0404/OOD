# library.py
from library_management_system.models.account import Member
from services.catalog import Catalog
from services.lending_service import LendingService
from services.reservation_service import ReservationService
from services.notification_service import NotificationService
# ... imports from models

class Library:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        
        # 1. Initialize Independent Services
        self.catalog = Catalog()
        self.reservation_service = ReservationService()
        self.notification_service = NotificationService()
        
        # 2. Initialize LendingService with dependencies
        self.lending_service = LendingService(
            reservation_service=self.reservation_service,
            notification_service=self.notification_service
        )
        
        self.members = {}
        self.librarians = {}

    def add_member(self, member: Member):
        self.members[member.barcode] = member
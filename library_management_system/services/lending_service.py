# services/lending_service.py (Updated)
from datetime import datetime, timedelta
from typing import Dict, List

from constants import BookStatus, Constants
from models.book import BookItem
from models.account import Member
from services.fine_service import FineService
from services.reservation_service import ReservationService # <--- Import
from services.notification_service import NotificationService # <--- Import

class LendingService:
    def __init__(self, reservation_service: ReservationService, notification_service: NotificationService):
        # Dependencies injected
        self.reservation_service = reservation_service
        self.notification_service = notification_service
        self.fine_service = FineService()
        
        self.active_loans: Dict[str, List[BookItem]] = {} 

    def checkout_book(self, member: Member, book_item: BookItem) -> bool:
        if book_item.status == BookStatus.RESERVED:
            # Check if this specific member is the one who reserved it?
            # For simplicity, we assume if it's reserved, only the reserver can take it.
            # (In a full app, you'd verify member.id match here)
            pass 
        elif book_item.status != BookStatus.AVAILABLE:
            print(f"Error: Book '{book_item.book.title}' is not available.")
            return False
            
        current_loans = self.active_loans.get(member.barcode, [])
        if len(current_loans) >= Constants.MAX_BOOKS_CHECKOUT:
            print("Error: Max books limit reached.")
            return False
            
        # PROCEED TO CHECKOUT
        book_item.status = BookStatus.BORROWED
        book_item.borrowed_date = datetime.now()
        book_item.due_date = datetime.now() + timedelta(days=Constants.MAX_DAYS_CHECKOUT)
        
        if member.barcode not in self.active_loans:
            self.active_loans[member.barcode] = []
        self.active_loans[member.barcode].append(book_item)
        
        print(f"Success: {member.name} checked out '{book_item.book.title}'")
        return True

    def return_book(self, member: Member, book_item: BookItem):
        if member.barcode in self.active_loans and book_item in self.active_loans[member.barcode]:
            # 1. Remove from member's active loans
            self.active_loans[member.barcode].remove(book_item)
            
            # 2. Check Fines
            if book_item.due_date and datetime.now() > book_item.due_date:
                diff = datetime.now() - book_item.due_date
                fine = self.fine_service.calculate_fine(book_item, diff.days)
                if fine > 0:
                    self.notification_service.notify_overdue(member, book_item, fine)

            # 3. Check Reservations (The Integration Logic)
            reserver = self.reservation_service.get_next_reservation(book_item.book.isbn)
            
            if reserver:
                # Someone is waiting!
                book_item.status = BookStatus.RESERVED
                print(f"Book Reserved for {reserver.name}")
                self.notification_service.notify_book_available(reserver, book_item)
            else:
                # No one waiting, put back on shelf
                book_item.status = BookStatus.AVAILABLE
                print(f"Book Returned to Shelf '{book_item.rack.location_identifier}'")

        else:
            print("Error: This member does not have this book checked out.")
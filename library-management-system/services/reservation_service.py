# services/reservation_service.py
from collections import defaultdict, deque
from typing import Dict, Deque

from models.account import Member
from models.book import Book

class ReservationService:
    def __init__(self):
        # Key: Book ISBN -> Value: Queue of Members waiting
        self.reservations: Dict[str, Deque[Member]] = defaultdict(deque)

    def make_reservation(self, member: Member, book: Book):
        # Add member to the back of the queue for this specific book title
        self.reservations[book.isbn].append(member)
        print(f"Reservation placed for {member.name} on '{book.title}'. Position in queue: {len(self.reservations[book.isbn])}")

    def get_next_reservation(self, isbn: str) -> Member | None:
        # Check if anyone is waiting for this ISBN
        if isbn in self.reservations and self.reservations[isbn]:
            return self.reservations[isbn].popleft() # First in, First out
        return None
    
    def cancel_reservation(self, member: Member, book: Book):
        if book.isbn in self.reservations:
            try:
                self.reservations[book.isbn].remove(member)
                print(f"Reservation canceled for {member.name}.")
            except ValueError:
                print("Member had no reservation for this book.")
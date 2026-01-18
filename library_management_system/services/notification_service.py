# services/notification_service.py
from models.account import Member
from models.book import BookItem

class NotificationService:
    def send_notification(self, member: Member, message: str):
        print(f"\n[ALERT] Sending Email to {member.email} ({member.name})...")
        print(f"        Message: {message}")
        print("------------------------------------------------------")

    def notify_book_available(self, member: Member, book_item: BookItem):
        message = f"Good news! The book '{book_item.book.title}' you reserved is now available. Please pick it up at {book_item.rack.location_identifier}."
        self.send_notification(member, message)

    def notify_overdue(self, member: Member, book_item: BookItem, fine_amount: float):
        message = f"URGENT: The book '{book_item.book.title}' is overdue. Current fine: ${fine_amount:.2f}. Please return it immediately."
        self.send_notification(member, message)
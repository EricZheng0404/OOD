from typing import List, Optional
from constants import BookStatus
from models.abstract import BarcodeEntity
from datetime import datetime
class Book:
    """Logical definition (Metadata) e.g., 'Harry Potter'"""
    def __init__(self, isbn: str, title: str, author: str, subject: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.subject = subject
        self.book_item_ids: List[str] = [] # List of barcodes associated with this title

class Rack:
    def __init__(self, number: int, location_identifier: str):
        self.number = number
        self.location_identifier = location_identifier

class BookItem(BarcodeEntity):
    """Physical copy on the shelf e.g., 'Harry Potter Copy #3'"""
    def __init__(self, barcode: str, book: Book, rack: Rack):
        super().__init__(barcode)
        self.book = book # Reference to the metadata
        self.status = BookStatus.AVAILABLE
        self.rack = rack
        self.borrowed_date: Optional[datetime] = None
        self.due_date: Optional[datetime] = None
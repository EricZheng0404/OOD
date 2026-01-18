from collections import defaultdict
from typing import List, Dict
from models.book import Book, BookItem

class Catalog:
    def __init__(self):
        self.books_by_isbn: Dict[str, Book] = {}
        self.book_items: Dict[str, BookItem] = {} # Key: Barcode
        
        # Search Indexes (Fast lookups)
        self.titles: Dict[str, List[Book]] = defaultdict(list)
        self.authors: Dict[str, List[Book]] = defaultdict(list)
        self.subjects: Dict[str, List[Book]] = defaultdict(list)

    def add_book_item(self, book_item: BookItem):
        book = book_item.book
        
        # Add to main storage
        if book.isbn not in self.books_by_isbn:
            self.books_by_isbn[book.isbn] = book
            # Add to indexes
            self.titles[book.title].append(book)
            self.authors[book.author].append(book)
            self.subjects[book.subject].append(book)
            
        self.book_items[book_item.barcode] = book_item
        book.book_item_ids.append(book_item.barcode)

    def search_by_title(self, title: str) -> List[Book]:
        return self.titles.get(title, [])
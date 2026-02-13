# main.py
from datetime import datetime
from constants import BookStatus
from models.book import Book, BookItem, Rack
from models.account import Member
from library import Library

def run_simulation():
    print("=== STARTING LIBRARY SIMULATION ===\n")

    # 1. Setup the Library System
    print("--- Setup ---")
    my_library = Library(name="City Library", address="123 Main St")
    
    # 2. Create a Logical Book (Metadata)
    harry_potter = Book(
        isbn="978-0747532743", 
        title="Harry Potter and the Philosopher's Stone", 
        author="J.K. Rowling", 
        subject="Fantasy"
    )
    # Add to catalog
    my_library.catalog.books_by_isbn[harry_potter.isbn] = harry_potter

    # 3. Create a Physical Copy (BookItem)
    shelf_a1 = Rack(number=1, location_identifier="A1")
    hp_copy_1 = BookItem(
        barcode="hp-copy-01", 
        book=harry_potter, 
        rack=shelf_a1
    )
    # Add physical copy to catalog
    my_library.catalog.add_book_item(hp_copy_1)
    print(f"Created Book: {harry_potter.title} (ID: {hp_copy_1.barcode})")

    # 4. Create Members
    bob = Member(barcode="user-bob", name="Bob Builder", email="bob@example.com")
    alice = Member(barcode="user-alice", name="Alice Wonderland", email="alice@example.com")
    my_library.add_member(bob)
    my_library.add_member(alice)
    print(f"Created Members: {bob.name}, {alice.name}\n")


    # --- SCENARIO START ---

    # Step 1: Bob checks out the book
    print("--- Step 1: Bob checks out the book ---")
    my_library.lending_service.checkout_book(member=bob, book_item=hp_copy_1)
    print("")
    # Step 2: Alice tries to reserve the book
    print("--- Step 2: Alice tries to reserve the book ---")
    my_library.reservation_service.make_reservation(member=alice, book=hp_copy_1.book)
    print("")
    # Step 3: Bob returns the book late
    print("--- Step 3: Bob returns the book late ---")
    # Simulate late return by manipulating due_date
    hp_copy_1.due_date = datetime.now().replace(year=datetime.now().year - 1)  # Set due date to last year
    my_library.lending_service.return_book(member=bob, book_item=hp_copy_1)
    print("")
    # --- SCENARIO END ---  
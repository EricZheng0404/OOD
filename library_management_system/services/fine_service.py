from datetime import datetime
from ..models.book import BookItem

class FineService:
    def calculate_fine(self, book_item: BookItem, days_overdue: int) -> float:
        # Simple logic: $0.50 per day
        fine_per_day = 0.50
        return days_overdue * fine_per_day
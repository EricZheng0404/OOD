from abc import ABC, abstractmethod
from datetime import datetime

class BarcodeEntity(ABC):
    """Abstract Mixin for anything that needs a physical barcode scan."""
    def __init__(self, barcode_str: str):
        self.barcode = barcode_str

class Person(ABC):
    """Base class for humans."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
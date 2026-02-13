from decimal import Decimal
from collections import deque

class ExchangeRateTable:
    def __init__(self):
        # "USD": {"RMB": 7.0}
        # This structure is better to triangulated relationship
        self.currencies: dict[str, dict[str, Decimal]] = {}

    def check_exchange_rate(self, from_currency, to_currency) -> Decimal:
        if from_currency not in self.currencies:
            raise KeyError(f"{from_currency} not supported")
        if to_currency not in self.currencies:
            raise KeyError(f"No exchange rate found")
        # To search from triangulated relationship. 
        # For example, we want USD -> RMB,
        # but we only have USD -> GBP and GBP -> RMB
        # We use BFS to iterate through the graph
        if from_currency == to_currency:
            return Decimal(1)
        q = deque([(from_currency, Decimal(1))])
        visited = {from_currency}
        while q:
            curr_currency, curr_rate = q.popleft()
            for neighbor in self.currencies[curr_currency]:
                if neighbor == to_currency:
                    return self.currencies[curr_currency][neighbor] * curr_rate
                if neighbor not in visited:
                    q.append((neighbor, curr_rate * self.currencies[curr_currency][neighbor]))
                    visited.add(neighbor)
        raise KeyError(f"Cannot find a rate between {from_currency} to {to_currency}")

    
    # Add/Update exchange rate between the two currencies
    def set_exchange_rate(self, from_currency, to_currency, rate):
        # Safer for Decimal
        rate = Decimal(str(rate))
        if rate <= 0:
            raise ValueError(f"Rate must be greater than 0")
        if from_currency not in self.currencies:
            self.currencies[from_currency] = {}
        if to_currency not in self.currencies:
            self.currencies[to_currency] = {}
        self.currencies[from_currency][to_currency] = rate
        self.currencies[to_currency][from_currency] = Decimal(1.0) / rate

class Bank:
    def __init__(self):
        self.users = {}
        self.exchange_rate: ExchangeRateTable = ExchangeRateTable()

    def request_exchange(self, user_id, from_currency, to_currency, amount):
        if user_id not in self.users:
            raise KeyError(f"user doesn't exist")
        user = self.users[user_id]
        # Check the validity of currencies
        if from_currency not in user.accounts:
            raise KeyError(f"from_currency not valid")
        if to_currency not in user.accounts:
            raise KeyError(f"in_currency not valid")
        # We get and calculate all the data
        from_account = user.accounts[from_currency]
        # There's a chance that this operation may fail
        exchange_rate = self.exchange_rate.check_exchange_rate(from_currency, to_currency)
        new_currency_amount = amount * exchange_rate
        to_account = user.accounts[to_currency]
        # We finally execute 
        from_account.withdraw((amount))
        to_account.deposit(new_currency_amount)

class User:
    def __init__(self, u_id):
        self.u_id = u_id
        self.accounts = {}
    
    def check_account(self, currency):
        return currency in self.accounts
    
    def add_account(self, currency):
        if currency in self.accounts:
            raise ValueError(f"Account already exists")
        self.accounts[currency] = Account(currency)


class Account:
    def __init__(self, currency):
        self.currency = currency
        self.balance = 0.0
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount



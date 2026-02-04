from decimal import Decimal

class ExchangeRateTable:
    def __init__(self):
        # "USD": {"RMB": 7.0}
        self.currencies: dict[str, dict[str, Decimal]] = {}

    def _validate_currency(self, currency):
        if currency not in self.currencies:
            raise KeyError("{currency} not exist")
        
    def check_exchange_rate(self, from_currency, to_currency):
        self._validate_currency(from_currency)
        self._validate_currency(to_currency)
        if to_currency not in self.currencies[from_currency]:
            raise KeyError("No exchange rate found")
        return self.currencies[from_currency][to_currency]
    
    def add_currency(self, currency):
        if currency in self.currencies:
            raise KeyError("{currency} already exist")
        self.currencies[currency] = {}
    
    # This could also be update function
    # This is 
    def add_exchange_rate(self, from_currency, to_currency, rate: Decimal):
        self._validate_currency(from_currency)
        self._validate_currency(to_currency)
        self.currencies[from_currency][to_currency] = rate
        self.currencies[to_currency][from_currency] = 1 / rate

class Bank:
    def __init__(self):
        self.users = {}
        self.exchange_rate = ExchangeRateTable()

    def request_exchange(self, user_id, from_currency, to_currency, exchange_rate_table: ExchangeRateTable, amount):
        if user_id not in self.users:
            raise KeyError("use doesn't exist")
        user = self.users[user_id]
        # Check the validity of currencies
        if from_currency not in user.accounts:
            raise KeyError("from_currency not valid")
        if to_currency not in user.accounts:
            raise KeyError("in_currency not valid")
        from_account = user[from_currency]
        from_account.withdraw(amount)
        exchange_rate = exchange_rate_table.check_exchange_rate(from_currency, to_currency)
        new_currency_amount = amount * exchange_rate
        to_account = user[to_currency]
        to_account.deposit(new_currency_amount)
class User:
    def __init__(self, u_id):
        self.u_id = u_id
        self.accounts = {}
    
    def check_account(self, currency):
        return currency in self.accounts
    
    def add_account(self, currency):
        if currency in self.accounts:
            raise ValueError("Account already exists")
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



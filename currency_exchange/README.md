# Currency Exchange System

A simple yet robust currency exchange system that simulates banking operations with multi-currency support and automatic exchange rate calculations through graph traversal.

## Overview

This system allows users to:
- Create bank accounts in multiple currencies
- Exchange money between different currencies
- Automatically find exchange rates through triangulated relationships (e.g., USD → GBP → RMB)

## Architecture

```
┌─────────────────────────────────────────────────┐
│                     Bank                         │
│  ┌─────────────────┐  ┌──────────────────────┐  │
│  │      Users      │  │  ExchangeRateTable   │  │
│  │   (dict)        │  │   (currency graph)   │  │
│  └────────┬────────┘  └──────────────────────┘  │
└───────────┼─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│                     User                         │
│  ┌─────────────────────────────────────────┐    │
│  │              Accounts (dict)             │    │
│  │   "USD" → Account   "EUR" → Account     │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│                   Account                        │
│   currency: str    balance: Decimal              │
└─────────────────────────────────────────────────┘
```

## Classes

### `ExchangeRateTable`
Manages exchange rates between currencies using a graph-based structure.

| Method | Description |
|--------|-------------|
| `set_exchange_rate(from_currency, to_currency, rate)` | Add or update exchange rate between two currencies (automatically sets inverse rate) |
| `check_exchange_rate(from_currency, to_currency)` | Get exchange rate using BFS to find path through currency graph |

### `Bank`
Central entity that manages users and exchange rates.

| Method | Description |
|--------|-------------|
| `request_exchange(user_id, from_currency, to_currency, amount)` | Execute currency exchange for a user |

### `User`
Represents a bank customer with multiple currency accounts.

| Method | Description |
|--------|-------------|
| `add_account(currency)` | Create a new account in specified currency |
| `check_account(currency)` | Check if account exists for currency |

### `Account`
Holds balance for a single currency.

| Method | Description |
|--------|-------------|
| `deposit(amount)` | Add funds to account |
| `withdraw(amount)` | Remove funds (raises error if insufficient) |

## Usage Example

```python
from currency_exchange import Bank, User

# Create bank and set up exchange rates
bank = Bank()
bank.exchange_rate.set_exchange_rate("USD", "EUR", 0.85)
bank.exchange_rate.set_exchange_rate("EUR", "GBP", 0.88)

# Create user with accounts
user = User("user_001")
user.add_account("USD")
user.add_account("EUR")
user.add_account("GBP")
bank.users["user_001"] = user

# Deposit initial funds
user.accounts["USD"].deposit(1000)

# Exchange USD to EUR
bank.request_exchange("user_001", "USD", "EUR", 100)

# Exchange USD to GBP (uses triangulated rate: USD → EUR → GBP)
bank.request_exchange("user_001", "USD", "GBP", 50)
```

## Design Decisions

1. **Composition-based Architecture**: Bank → Users → Accounts hierarchy using composition relationships for clear ownership and encapsulation.

2. **Separate ExchangeRateTable Class**: Exchange rate logic is isolated in its own class under Bank, as only the bank should control rate data.

3. **Graph-based Exchange Rates**: Rates are stored as a bidirectional graph, enabling automatic triangulated conversions (e.g., USD → GBP → RMB) using BFS.

4. **Automatic Inverse Rates**: When setting a rate, the inverse is automatically calculated and stored (e.g., setting USD→EUR at 0.85 automatically sets EUR→USD at 1/0.85).

## Key Takeaways

1. **Use `decimal.Decimal` for Currency**: Avoids floating-point precision errors that can cause financial discrepancies.

2. **Graph-based Rate Lookup**: Enables indirect conversions without explicitly defining every currency pair. BFS ensures the shortest path is found.

3. **Input Validation**: Always validate inputs—rates must be positive, accounts must exist, and balances must be sufficient.

4. **Atomic Operations**: In `request_exchange()`, all validations (rate lookup, balance check) are performed **before** any state changes. This prevents partial execution if any step fails.

5. **Safe Decimal Conversion**: Use `Decimal(str(float))` instead of `Decimal(float)` to avoid floating-point representation issues.

## Potential Enhancements

- **Transaction History**: Track all exchanges with timestamps
- **Transaction Fees**: Add configurable exchange fees
- **Rate Caching**: Cache computed triangulated rates for performance
- **Concurrent Access**: Add locking mechanisms for thread safety
- **Rate Expiry**: Support time-based exchange rate updates

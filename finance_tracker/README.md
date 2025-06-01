# Personal Finance Tracker CLI

A command-line personal finance tracker to help you manage your income and expenses.

## Features

- Create and manage user profiles
- Record income and expense transactions
- Categorize transactions
- View transaction history with filters
- Get monthly summaries (income, expenses, balance)
- Delete transactions or entire profiles

## Installation

1. Clone this repository
2. Install Pipenv if you don't have it: `pip install pipenv`
3. Set up the virtual environment: `pipenv install`
4. Install the package in development mode: `pipenv run pip install -e .`

## Usage

After installation, you can use the CLI with the command `finance` followed by any of these commands:

- `add-user`: Create a new user profile
- `remove-user`: Delete a user profile
- `add-transaction`: Add a new transaction
- `view-transactions`: View transactions with filters
- `monthly-summary`: View monthly summary
- `remove-transaction`: Delete a transaction

Example:
```bash
finance add-user --name "John Doe" --email "john@example.com"

import click
from datetime import datetime
from typing import List, Dict
from .models import session, User, Transaction
from .crud import (
    create_user, get_user_by_email, delete_user,
    create_transaction, get_user_transactions,
    get_transactions_by_filter, get_monthly_summary,
    delete_transaction
)

@click.group()
def cli():
    """Personal Finance Tracker CLI"""
    pass

@cli.command()
@click.option('--name', prompt='Your name', help='Your full name')
@click.option('--email', prompt='Your email', help='Your email address')
def add_user(name, email):
    """Create a new user profile"""
    success, message = create_user(name, email)
    click.echo(message)

@cli.command()
@click.option('--email', prompt='Your email', help='Your registered email')
def remove_user(email):
    """Delete a user profile and all transactions"""
    user = get_user_by_email(email)
    if not user:
        click.echo("User not found!")
        return
    
    if click.confirm(f"Are you sure you want to delete {user.name}'s profile and ALL transactions?"):
        success, message = delete_user(user.id)
        click.echo(message)
    else:
        click.echo("Operation cancelled.")

@cli.command()
@click.option('--email', prompt='Your email', help='Your registered email')
@click.option('--amount', prompt='Amount', type=float, help='Transaction amount')
@click.option('--type', prompt='Type (income/expense)', type=click.Choice(['income', 'expense']), help='Transaction type')
@click.option('--category', prompt='Category', help='Transaction category (e.g., Salary, Food)')
@click.option('--description', prompt='Description (optional)', default='', help='Transaction description')
@click.option('--date', prompt='Date (YYYY-MM-DD, leave blank for today)', default='', help='Transaction date')
def add_transaction(email, amount, type, category, description, date):
    """Add a new transaction"""
    user = get_user_by_email(email)
    if not user:
        click.echo("User not found!")
        return
    
    success, message = create_transaction(
        user_id=user.id,
        amount=amount,
        transaction_type=type,
        category=category,
        description=description,
        date=date if date else None
    )
    click.echo(message)

@cli.command()
@click.option('--email', prompt='Your email', help='Your registered email')
@click.option('--type', default=None, help='Filter by type (income/expense)')
@click.option('--category', default=None, help='Filter by category')
@click.option('--start-date', default=None, help='Start date (YYYY-MM-DD)')
@click.option('--end-date', default=None, help='End date (YYYY-MM-DD)')
def view_transactions(email, type, category, start_date, end_date):
    """View transactions with optional filters"""
    user = get_user_by_email(email)
    if not user:
        click.echo("User not found!")
        return
    
    transactions = get_transactions_by_filter(
        user_id=user.id,
        transaction_type=type,
        category=category,
        start_date=start_date,
        end_date=end_date
    )
    
    if not transactions:
        click.echo("No transactions found.")
        return
    
    click.echo(f"\nTransactions for {user.name}:")
    click.echo("-" * 80)
    for t in transactions:
        click.echo(f"ID: {t.id} | Date: {t.date} | Type: {t.type.upper()} | Amount: {t.amount} | Category: {t.category}")
        if t.description:
            click.echo(f"Description: {t.description}")
        click.echo("-" * 80)

@cli.command()
@click.option('--email', prompt='Your email', help='Your registered email')
@click.option('--year', prompt='Year', type=int, help='Year for summary')
@click.option('--month', prompt='Month (1-12)', type=click.IntRange(1, 12), help='Month for summary')
def monthly_summary(email, year, month):
    """View monthly summary (income, expenses, balance)"""
    user = get_user_by_email(email)
    if not user:
        click.echo("User not found!")
        return
    
    summary = get_monthly_summary(user.id, year, month)
    
    click.echo(f"\nMonthly Summary for {user.name} - {month}/{year}:")
    click.echo("-" * 40)
    click.echo(f"Income: {summary['income']}")
    click.echo(f"Expenses: {summary['expenses']}")
    click.echo(f"Balance: {summary['balance']}")
    click.echo("-" * 40)

@cli.command()
@click.option('--email', prompt='Your email', help='Your registered email')
@click.option('--id', prompt='Transaction ID', type=int, help='ID of transaction to delete')
def remove_transaction(email, id):
    """Delete a transaction"""
    user = get_user_by_email(email)
    if not user:
        click.echo("User not found!")
        return
    
    transaction = session.query(Transaction).filter(
        Transaction.id == id,
        Transaction.user_id == user.id
    ).first()
    
    if not transaction:
        click.echo("Transaction not found or doesn't belong to you!")
        return
    
    if click.confirm(f"Are you sure you want to delete this transaction?\n{transaction}"):
        success, message = delete_transaction(id)
        click.echo(message)
    else:
        click.echo("Operation cancelled.")

if __name__ == '__main__':
    cli()
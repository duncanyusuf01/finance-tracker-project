from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .models import session, User, Transaction
from typing import List, Dict, Optional, Tuple

def create_user(name: str, email: str) -> Tuple[bool, str]:
    """Create a new user"""
    try:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        return True, f"User {name} created successfully!"
    except IntegrityError:
        session.rollback()
        return False, "Email already exists. Please use a different email."
    except Exception as e:
        session.rollback()
        return False, f"Error creating user: {str(e)}"

def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email"""
    return session.query(User).filter(User.email == email).first()

def delete_user(user_id: int) -> Tuple[bool, str]:
    """Delete a user and all their transactions"""
    user = session.query(User).get(user_id)
    if not user:
        return False, "User not found"
    
    try:
        session.delete(user)
        session.commit()
        return True, "User and all associated transactions deleted successfully"
    except Exception as e:
        session.rollback()
        return False, f"Error deleting user: {str(e)}"

def create_transaction(
    user_id: int,
    amount: float,
    transaction_type: str,
    category: str,
    description: str = "",
    date: str = None
) -> Tuple[bool, str]:
    """Create a new transaction"""
    try:
        if not date:
            transaction_date = datetime.now().date()
        else:
            transaction_date = datetime.strptime(date, "%Y-%m-%d").date()
            
        transaction = Transaction(
            amount=amount,
            type=transaction_type,
            category=category,
            description=description,
            date=transaction_date,
            user_id=user_id
        )
        
        session.add(transaction)
        session.commit()
        return True, "Transaction added successfully!"
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."
    except Exception as e:
        session.rollback()
        return False, f"Error creating transaction: {str(e)}"

def get_user_transactions(user_id: int) -> List[Transaction]:
    """Get all transactions for a user"""
    return session.query(Transaction).filter(Transaction.user_id == user_id).all()

def get_transactions_by_filter(
    user_id: int,
    transaction_type: str = None,
    category: str = None,
    start_date: str = None,
    end_date: str = None
) -> List[Transaction]:
    """Get transactions with optional filters"""
    query = session.query(Transaction).filter(Transaction.user_id == user_id)
    
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type)
    if category:
        query = query.filter(Transaction.category == category)
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        query = query.filter(Transaction.date <= end_date)
    
    return query.all()

def get_monthly_summary(user_id: int, year: int, month: int) -> Dict[str, float]:
    """Get monthly summary (income, expenses, balance)"""
    transactions = session.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date >= datetime(year, month, 1).date(),
        Transaction.date <= datetime(year, month + 1, 1).date() if month < 12 
        else datetime(year + 1, 1, 1).date()
    ).all()
    
    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expenses
    
    return {
        'income': income,
        'expenses': expenses,
        'balance': balance
    }

def delete_transaction(transaction_id: int) -> Tuple[bool, str]:
    """Delete a transaction"""
    transaction = session.query(Transaction).get(transaction_id)
    if not transaction:
        return False, "Transaction not found"
    
    try:
        session.delete(transaction)
        session.commit()
        return True, "Transaction deleted successfully"
    except Exception as e:
        session.rollback()
        return False, f"Error deleting transaction: {str(e)}"
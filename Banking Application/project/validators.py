import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_name(name):
        if not name or len(name) < 2 or not name.replace(" ", "").isalpha():
            raise ValueError("Invalid name. Name should contain only letters and be at least 2 characters long.")
        return True

    @staticmethod
    def validate_contact(contact):
        if not re.match(r'^\d{10}$', contact):
            raise ValueError("Invalid contact number. Should be 10 digits.")
        return True

    @staticmethod
    def validate_email(email):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email format.")
        return True

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character.")
        return True

    @staticmethod
    def validate_balance(balance):
        try:
            balance = float(balance)
            if balance < 2000:
                raise ValueError("Initial balance must be at least 2000.")
            return True
        except ValueError:
            raise ValueError("Invalid balance amount.")
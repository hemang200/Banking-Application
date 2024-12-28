import random
from validators import Validators
from database import Database

class User:
    def __init__(self):
        self.db = Database()
        self.validators = Validators()

    def generate_account_number(self):
        while True:
            account_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            # Check if account number already exists
            self.db.cursor.execute("SELECT account_number FROM users WHERE account_number = %s", (account_number,))
            if not self.db.cursor.fetchone():
                return account_number

    def create_user(self, name, dob, city, password, initial_balance, contact, email, address):
        try:
            # Validate all inputs
            self.validators.validate_name(name)
            self.validators.validate_contact(contact)
            self.validators.validate_email(email)
            self.validators.validate_password(password)
            self.validators.validate_balance(initial_balance)

            account_number = self.generate_account_number()

            query = """
                INSERT INTO users 
                (name, account_number, dob, city, password, balance, contact_number, email, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, account_number, dob, city, password, initial_balance, contact, email, address)
            
            self.db.cursor.execute(query, values)
            self.db.conn.commit()
            
            return account_number
            
        except Exception as e:
            self.db.conn.rollback()
            raise e

    def show_user(self, account_number):
        query = "SELECT * FROM users WHERE account_number = %s"
        self.db.cursor.execute(query, (account_number,))
        return self.db.cursor.fetchone()
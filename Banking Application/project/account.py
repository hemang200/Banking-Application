from database import Database

class Account:
    def __init__(self):
        self.db = Database()

    def login(self, account_number, password):
        query = "SELECT * FROM users WHERE account_number = %s AND password = %s AND is_active = TRUE"
        self.db.cursor.execute(query, (account_number, password))
        return self.db.cursor.fetchone()

    def get_balance(self, account_number):
        query = "SELECT balance FROM users WHERE account_number = %s"
        self.db.cursor.execute(query, (account_number,))
        result = self.db.cursor.fetchone()
        return result[0] if result else None

    def credit_amount(self, account_number, amount):
        try:
            # Update balance
            update_query = "UPDATE users SET balance = balance + %s WHERE account_number = %s"
            self.db.cursor.execute(update_query, (amount, account_number))

            # Record transaction
            trans_query = """
                INSERT INTO transactions (account_number, transaction_type, amount)
                VALUES (%s, 'credit', %s)
            """
            self.db.cursor.execute(trans_query, (account_number, amount))
            
            self.db.conn.commit()
            return True
        except Exception as e:
            self.db.conn.rollback()
            raise e

    def debit_amount(self, account_number, amount):
        try:
            # Check balance
            current_balance = self.get_balance(account_number)
            if current_balance < amount:
                raise ValueError("Insufficient balance")

            # Update balance
            update_query = "UPDATE users SET balance = balance - %s WHERE account_number = %s"
            self.db.cursor.execute(update_query, (amount, account_number))

            # Record transaction
            trans_query = """
                INSERT INTO transactions (account_number, transaction_type, amount)
                VALUES (%s, 'debit', %s)
            """
            self.db.cursor.execute(trans_query, (account_number, amount))
            
            self.db.conn.commit()
            return True
        except Exception as e:
            self.db.conn.rollback()
            raise e

    def transfer_amount(self, from_account, to_account, amount):
        try:
            self.debit_amount(from_account, amount)
            self.credit_amount(to_account, amount)
            return True
        except Exception as e:
            raise e

    def get_transactions(self, account_number):
        query = "SELECT * FROM transactions WHERE account_number = %s ORDER BY transaction_date DESC"
        self.db.cursor.execute(query, (account_number,))
        return self.db.cursor.fetchall()

    def change_password(self, account_number, new_password):
        query = "UPDATE users SET password = %s WHERE account_number = %s"
        self.db.cursor.execute(query, (new_password, account_number))
        self.db.conn.commit()

    def update_profile(self, account_number, city=None, contact=None, email=None, address=None):
        updates = []
        values = []
        if city:
            updates.append("city = %s")
            values.append(city)
        if contact:
            updates.append("contact_number = %s")
            values.append(contact)
        if email:
            updates.append("email = %s")
            values.append(email)
        if address:
            updates.append("address = %s")
            values.append(address)
        
        if updates:
            query = f"UPDATE users SET {', '.join(updates)} WHERE account_number = %s"
            values.append(account_number)
            self.db.cursor.execute(query, tuple(values))
            self.db.conn.commit()

    def toggle_account_status(self, account_number):
        query = "UPDATE users SET is_active = NOT is_active WHERE account_number = %s"
        self.db.cursor.execute(query, (account_number,))
        self.db.conn.commit()
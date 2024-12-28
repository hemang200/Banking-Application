import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="solana.me@2024"
            )
            self.cursor = self.conn.cursor()
            
            # Create database if not exists
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS banking_system")
            self.cursor.execute("USE banking_system")
            
            # Create required tables
            self._create_tables()
            
        except Error as e:
            print(f"Error: {e}")

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                account_number VARCHAR(10) UNIQUE NOT NULL,
                dob DATE NOT NULL,
                city VARCHAR(50) NOT NULL,
                password VARCHAR(100) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL,
                contact_number VARCHAR(15) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                address TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_number VARCHAR(10),
                transaction_type ENUM('credit', 'debit', 'transfer') NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                recipient_account VARCHAR(10),
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_number) REFERENCES users(account_number)
            )
        """)
        
        self.conn.commit()
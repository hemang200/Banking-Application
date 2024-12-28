from user import User
from account import Account
from menus import Menus
from exceptions import *

def handle_user_creation(user_service):
    try:
        print("\n=== ADD USER ===")
        name = input("Enter name: ")
        dob = input("Enter DOB (YYYY-MM-DD): ")
        city = input("Enter city: ")
        password = input("Enter password: ")
        initial_balance = float(input("Enter initial balance (min 2000): "))
        contact = input("Enter contact number: ")
        email = input("Enter email: ")
        address = input("Enter address: ")
        
        account_number = user_service.create_user(
            name, dob, city, password, initial_balance,
            contact, email, address
        )
        print(f"\nUser created successfully! Account number: {account_number}")
    
    except Exception as e:
        print(f"Error: {e}")

def handle_show_user(user_service):
    try:
        account_number = input("Enter account number: ")
        user_data = user_service.show_user(account_number)
        if not user_data:
            raise UserNotFoundError("User not found!")
            
        print("\n=== USER INFORMATION ===")
        print(f"Name: {user_data[1]}")
        print(f"Account Number: {user_data[2]}")
        print(f"City: {user_data[4]}")
        print(f"Balance: {user_data[6]}")
        print(f"Contact: {user_data[7]}")
        print(f"Email: {user_data[8]}")
        print(f"Address: {user_data[9]}")
        print(f"Account Status: {'Active' if user_data[10] else 'Inactive'}")
    
    except Exception as e:
        print(f"Error: {e}")

def handle_logged_in_user(account_service, account_number, user_name):
    print(f"\nWelcome {user_name}!")
    
    while True:
        try:
            login_choice = Menus.login_menu()
            
            if login_choice == '1':
                balance = account_service.get_balance(account_number)
                print(f"\nCurrent Balance: {balance}")
            
            elif login_choice == '2':
                transactions = account_service.get_transactions(account_number)
                print("\n=== TRANSACTION HISTORY ===")
                for t in transactions:
                    print(f"Type: {t[2]}, Amount: {t[3]}, Date: {t[5]}")
            
            elif login_choice == '3':
                amount = float(input("Enter amount to credit: "))
                if account_service.credit_amount(account_number, amount):
                    print("Amount credited successfully!")
            
            elif login_choice == '4':
                amount = float(input("Enter amount to debit: "))
                if account_service.debit_amount(account_number, amount):
                    print("Amount debited successfully!")
            
            elif login_choice == '5':
                to_account = input("Enter recipient's account number: ")
                amount = float(input("Enter amount to transfer: "))
                if account_service.transfer_amount(account_number, to_account, amount):
                    print("Amount transferred successfully!")
            
            elif login_choice == '6':
                account_service.toggle_account_status(account_number)
                print("Account status updated successfully!")
            
            elif login_choice == '7':
                new_password = input("Enter new password: ")
                account_service.change_password(account_number, new_password)
                print("Password changed successfully!")
            
            elif login_choice == '8':
                print("\nEnter new details (press enter to skip):")
                city = input("City: ")
                contact = input("Contact: ")
                email = input("Email: ")
                address = input("Address: ")
                account_service.update_profile(
                    account_number,
                    city or None,
                    contact or None,
                    email or None,
                    address or None
                )
                print("Profile updated successfully!")
            
            elif login_choice == '9':
                print("Logged out successfully!")
                break
        
        except Exception as e:
            print(f"Error: {e}")

def main():
    user_service = User()
    account_service = Account()
    
    while True:
        choice = Menus.main_menu()
        
        if choice == '1':
            handle_user_creation(user_service)
        
        elif choice == '2':
            handle_show_user(user_service)
        
        elif choice == '3':
            try:
                account_number = input("Enter account number: ")
                password = input("Enter password: ")
                
                user_data = account_service.login(account_number, password)
                if not user_data:
                    raise InvalidCredentialsError("Invalid credentials!")
                
                handle_logged_in_user(account_service, account_number, user_data[1])
            
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '4':
            print("Thank you for using our banking system!")
            break

if __name__ == "__main__":
    main()
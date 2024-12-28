class Menus:
    @staticmethod
    def main_menu():
        print("\n=== BANKING SYSTEM ===")
        print("1. Add User")
        print("2. Show User")
        print("3. Login")
        print("4. Exit")
        return input("Choose an option: ")

    @staticmethod
    def login_menu():
        print("\n=== LOGIN MENU ===")
        print("1. Show Balance")
        print("2. Show Transactions")
        print("3. Credit Amount")
        print("4. Debit Amount")
        print("5. Transfer Amount")
        print("6. Toggle Account Status")
        print("7. Change Password")
        print("8. Update Profile")
        print("9. Logout")
        return input("Choose an option: ")
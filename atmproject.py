import random
class ATM:
    def main_menu(self):
        while True:
            print("Automatic Teller Machine")
            print("\nMAIN MENU:")
            print("1. Create Account")
            print("2. Check in")
            print("3. Exit")

            press = input("Enter your choice: ")

            if press == '1':
                self.create_account()
            elif press == '2':
                self.check_in()
            elif press == '3':
                print("existing--\ngood bye")
                break
            else:
                print("Invalid choice\ntry again.")

    def create_account(self):
        name = input("Enter your name: ")
        deposit = float(input("Enter deposit amount (more than 50): "))
        pin_code = input("Enter 4-digit PIN code: ")

        if len(pin_code) != 4:
            print("Invalid PIN code. It must be 4 digits.")
            return

        user_id = str(random.randint(100000000, 999999999))
        username = name + str(random.randint(1, 99))
        status = "ACTIVE"
        currency = "PKR"
        statement = [{"transaction": "Deposit", "amount": deposit, "balance": deposit}]

        user_info = {
            "name": name,
            "deposit": deposit,
            "pin_code": pin_code,
            "id": user_id,
            "username": username,
            "status": status,
            "currency": currency,
            "statement": statement,
        }

        self.users[username] = user_info
        self.save_to_file(username, user_info)

        print(f"Account created successfully!\nYour username: {username}\nUser ID: {user_id}")

    def check_in(self):
        username = input("Enter your username: ")
        pin_code = input("Enter your PIN code: ")

        if (username not in self.users
                or self.users[username]["status"] == "BLOCKED"
                or self.users[username]["pin_code"] != pin_code):
            print("Invalid username or PIN code. User not found or blocked.")
            return

        self.current_user =self.users[username]

        while True:
            print("\nSUB MENU:")
            print("1. Account Detail")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Update PIN")
            print("5. Check Statement")
            print("6. Logout")

            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                self.account_detail()
            elif sub_choice == '2':
                self.deposit()
            elif sub_choice == '3':
                self.withdraw()
            elif sub_choice == '4':
                self.update_pin()
            elif sub_choice == '5':
                self.check_statement()
            elif sub_choice == '6':
                self.current_user = None
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please try again.")

    def __init__(account):
        account.users = {}
        account.current_user = None
    def account_detail(self):
        user = self.current_user
        print(f"Name: {user['name']}")
        print(f"Username: {user['username']}")
        print(f"Status: {user['status']}")
        print(f"Balance: {user['deposit']} {user['currency']}")

    def deposit(self):
        user = self.current_user
        amount = float(input("Enter the amount to deposit: "))

        if amount < 50:
            print("Amount must be at least 50.")
            return

        user['deposit'] += amount
        user['statement'].append({"transaction": "Deposit", "amount": amount, "balance": user['deposit']})
        self.save_to_file(user['username'], user)

        print(f"Deposited {amount} {user['currency']} successfully.")
        print(f"Updated balance: {user['deposit']} {user['currency']}")

    def withdraw(self):
        user = self.current_user
        if user['status'] == "BLOCKED":
            print("Blocked user cannot withdraw. Contact support to unblock your account.")
            return

        amount = float(input("Enter the amount to withdraw: "))
        tax = 0.01 * amount

        if amount + tax > user['deposit']:
            print("Insufficient balance.")
            return

        user['deposit'] -= (amount + tax)
        user['statement'].append({"transaction": "Withdraw", "amount": amount, "balance": user['deposit']})
        self.save_to_file(user['username'], user)

        print(f"Withdrew {amount} {user['currency']} successfully.")
        print(f"Updated balance: {user['deposit']} {user['currency']}")

    def update_pin(self):
        user = self.current_user
        old_pin = input("Enter your old PIN code: ")

        if old_pin != user['pin_code']:
            print("Incorrect old PIN code. PIN update failed.")
            return

        new_pin = input("Enter your new 4-digit PIN code: ")

        if len(new_pin) != 4 or not new_pin.isdigit():
            print("Invalid PIN code. It must be 4 digits.")
            return

        user['pin_code'] = new_pin
        self.save_to_file(user['username'], user)

        print("PIN code updated successfully.")

    def check_statement(self):
        user = self.current_user
        username = user['username']
        statement_filename = f"{username}_statement.txt"

        with open(statement_filename, 'w') as file:
            for entry in user['statement']:
                file.write(f"Transaction: {entry['transaction']}, Amount: {entry['amount']}, Balance: {entry['balance']}\n")

        print(f"Statement saved to {statement_filename}.")

    def save_to_file(self, username, user_info):
        with open('users.txt', 'a') as file:
            file.write(f"{username}: {user_info}\n")

if __name__ == "__main__":
    atm = ATM()
    atm.main_menu()


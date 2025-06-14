import tkinter as tk
from tkinter import messagebox

class BankingException(Exception):
    pass

class NotEnoughMoney(BankingException):
    pass

class WrongAmount(BankingException):
    pass

class CustomerAccount:
    def __init__(self, account_holder, starting_balance=0, phone_credit=0):
        self.account_holder = account_holder
        self.current_balance = starting_balance
        self.phone_credit = phone_credit
    
    def add_money(self, deposit_amount):
        if deposit_amount <= 0:
            raise WrongAmount("Please enter positive value")
        self.current_balance += deposit_amount
    
    def take_money(self, withdrawal_amount):
        if withdrawal_amount <= 0:
            raise WrongAmount("Please enter positive value")
        if withdrawal_amount > self.current_balance:
            raise NotEnoughMoney("Insufficient funds")
        self.current_balance -= withdrawal_amount
    
    def send_money(self, transfer_amount, destination_account):
        if transfer_amount <= 0:
            raise WrongAmount("Please enter positive value")
        if transfer_amount > self.current_balance:
            raise NotEnoughMoney("Insufficient funds")
        self.current_balance -= transfer_amount
        destination_account.current_balance += transfer_amount
    
    def add_phone_credit(self, topup_amount):
        if topup_amount <= 0:
            raise WrongAmount("Please enter positive value")
        if topup_amount > self.current_balance:
            raise NotEnoughMoney("Insufficient funds")
        self.current_balance -= topup_amount
        self.phone_credit += topup_amount
    
    def account_details(self):
        details = f"Account Holder: {self.account_holder}\n"
        details += f"Current Balance: ${self.current_balance:.2f}\n"
        details += f"Phone Credit: ${self.phone_credit:.2f}"
        return details

class BankingApp:
    def __init__(self, main_window):
        self.main_window = main_window
        main_window.title("City Bank")
        
        self.all_accounts = {
            '2001': CustomerAccount("tashi yangchen", 2000),
            '2002': CustomerAccount("yangchen tashi", 1200)
        }
        
        self.active_account = None
        self.setup_gui()
    
    def setup_gui(self):
        account_frame = tk.LabelFrame(self.main_window, text="Account Access")
        account_frame.pack(padx=10, pady=5, fill="x")
        
        tk.Label(account_frame, text="Account Number:").grid(row=0, column=0)
        self.account_input = tk.Entry(account_frame)
        self.account_input.grid(row=0, column=1)
        self.access_button = tk.Button(
            account_frame,
            text="Access",
            command=self.verify_account
        )
        self.access_button.grid(row=0, column=2, padx=5)
        self.details_display = tk.Label(
            self.main_window,
            text="Please enter your account number",
            relief="groove",
            padx=5,
            pady=5
        )
        self.details_display.pack(padx=10, pady=5, fill="x")
        operations_frame = tk.LabelFrame(self.main_window, text="Banking Operations")
        operations_frame.pack(padx=10, pady=5, fill="both", expand=True)
        tk.Label(operations_frame, text="Amount ($):").grid(row=0, column=0)
        self.amount_input = tk.Entry(operations_frame)
        self.amount_input.grid(row=0, column=1)
        tk.Label(operations_frame, text="Target Account:").grid(row=1, column=0)
        self.target_account_input = tk.Entry(operations_frame)
        self.target_account_input.grid(row=1, column=1)
        button_config = {'padx': 6, 'pady': 3, 'width': 12}
        self.deposit_button = tk.Button(
            operations_frame,
            text="Deposit",
            command=self.process_deposit,
            **button_config
        )
        self.deposit_button.grid(row=2, column=0, pady=4)
        self.withdraw_button = tk.Button(
            operations_frame,
            text="Withdraw",
            command=self.process_withdrawal,
            **button_config
        )
        self.withdraw_button.grid(row=2, column=1, pady=4)
        self.transfer_button = tk.Button(
            operations_frame,
            text="Transfer",
            command=self.process_transfer,
            **button_config
        )
        self.transfer_button.grid(row=3, column=0, pady=4)
        
        self.phone_button = tk.Button(
            operations_frame,
            text="Phone Credit",
            command=self.process_phone_topup,
            **button_config
        )
        self.phone_button.grid(row=3, column=1, pady=4)
        self.disable_operations()
    def disable_operations(self):
        for btn in [self.deposit_button, self.withdraw_button,
                   self.transfer_button, self.phone_button]:
            btn.config(state=tk.DISABLED)
    def enable_operations(self):
        for btn in [self.deposit_button, self.withdraw_button,
                   self.transfer_button, self.phone_button]:
            btn.config(state=tk.NORMAL)
    def verify_account(self):
        account_number = self.account_input.get().strip()
        if account_number in self.all_accounts:
            self.active_account = self.all_accounts[account_number]
            self.update_account_display()
            self.enable_operations()
            messagebox.showinfo("Welcome", f"Hello {self.active_account.account_holder}!")
        else:
            messagebox.showerror("Error", "Account not found in our records")
    
    def update_account_display(self):
        if self.active_account:
            self.details_display.config(
                text=self.active_account.account_details()
            )
    
    def get_valid_amount(self):
        try:
            amount = float(self.amount_input.get())
            if amount <= 0:
                raise WrongAmount("Amount must be positive")
            return amount
        except ValueError:
            raise WrongAmount("Please enter a valid number")
    def process_deposit(self):
        try:
            amount = self.get_valid_amount()
            self.active_account.add_money(amount)
            self.update_account_display()
            messagebox.showinfo("Success", f"Deposited ${amount:.2f}")
        except BankingException as e:
            messagebox.showerror("Transaction Failed", str(e))
    def process_withdrawal(self):
        try:
            amount = self.get_valid_amount()
            self.active_account.take_money(amount)
            self.update_account_display()
            messagebox.showinfo("Success", f"Withdrew ${amount:.2f}")
        except BankingException as e:
            messagebox.showerror("Transaction Failed", str(e))
    
    def process_transfer(self):
        try:
            amount = self.get_valid_amount()
            target_account = self.target_account_input.get().strip()
            if target_account not in self.all_accounts:
                raise WrongAmount("Target account not found")
            if target_account == self.account_input.get().strip():
                raise WrongAmount("Cannot transfer to same account")
            self.active_account.send_money(amount, self.all_accounts[target_account])
            self.update_account_display()
            messagebox.showinfo("Success", f"Transferred ${amount:.2f} to account {target_account}")
        except BankingException as e:
            messagebox.showerror("Transfer Failed", str(e))
    
    def process_phone_topup(self):
        try:
            amount = self.get_valid_amount()
            self.active_account.add_phone_credit(amount)
            self.update_account_display()
            messagebox.showinfo("Success", f"Added ${amount:.2f} to phone credit")
        except BankingException as e:
            messagebox.showerror("Top-Up Failed", str(e))

if __name__ == "__main__":
    application_window = tk.Tk()
    banking_app = BankingApp(application_window)
    application_window.mainloop()
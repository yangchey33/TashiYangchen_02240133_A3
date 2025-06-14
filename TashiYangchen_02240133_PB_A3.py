import unittest
from TashiYangchen_02240133_PA_A3 import CustomerAccount, WrongAmount, NotEnoughMoney  

class CustomerAccountTests(unittest.TestCase):
    def setUp(self):
        self.account1 = CustomerAccount("tashi yangchen", 2000.00)
        self.account2 = CustomerAccount("yangchen tashi", 1200.00)
    
    def test_account_creation(self):
        self.assertEqual(self.account1.account_holder, "tashi yangchen")
        self.assertEqual(self.account1.current_balance, 2000.00)
        self.assertEqual(self.account1.phone_credit, 0.00)
    
    def test_deposit_operation(self):
        self.account1.add_money(300.50)
        self.assertEqual(self.account1.current_balance, 2300.50)
    
    def test_invalid_deposits(self):
        with self.assertRaises(WrongAmount):
            self.account1.add_money(-100)  
        with self.assertRaises(WrongAmount):
            self.account1.add_money(0)     
    
    def test_withdraw_operation(self):
        self.account1.take_money(200.25)
        self.assertEqual(self.account1.current_balance, 1799.75)
    
    def test_insufficient_funds(self):
        with self.assertRaises(NotEnoughMoney):
            self.account1.take_money(2500)  # More than balance
    
    def test_invalid_withdrawals(self):
        with self.assertRaises(WrongAmount):
            self.account1.take_money(-50)  # Negative amount
        with self.assertRaises(WrongAmount):
            self.account1.take_money(0)    # Zero amount
    
    def test_transfer_operation(self):
        self.account1.send_money(400, self.account2)
        self.assertEqual(self.account1.current_balance, 1600.00)
        self.assertEqual(self.account2.current_balance, 1600.00)
    
    def test_phone_topup(self):
        self.account1.add_phone_credit(150)
        self.assertEqual(self.account1.current_balance, 1850.00)
        self.assertEqual(self.account1.phone_credit, 150.00)
    
    def test_account_details(self):
        details = self.account1.account_details()
        self.assertIn("tashi yangchen", details)
        self.assertIn("2000.00", details)
        self.assertIn("0.00", details)

if __name__ == '__main__':
    print("Running CustomerAccount test suite...")
    unittest.main()
from debit_card import DebitCard, DebitCardSystem
import unittest


class TestDebitCardMethods(unittest.TestCase):

    def test_no_account_id(self):
        self.assertFalse(DebitCard().account_id)

    def test_valid_account_id(self):
        dc = DebitCard()
        dc.create_account(1)
        self.assertTrue(dc.account_id)

    def test_initial_balance(self):
        dc = DebitCard()
        self.assertEqual(dc.check_balance(), 0)

    def test_create_account_bad_balance(self):
        dc = DebitCard()
        with self.assertRaises(AssertionError):
            dc.create_account(-1)

    def test_create_account_bad_balance_format(self):
        dc = DebitCard()
        with self.assertRaises(ValueError):
            dc.create_account('one')

    def test_create_account_good(self):
        dc = DebitCard()
        dc.create_account(45)
        self.assertEqual(dc.check_balance(), 45)

    def test_charge_over(self):
        dc = DebitCard()
        dc.create_account(45)
        with self.assertRaises(AssertionError):
            dc.charge(amount=46)

    def test_charge_under(self):
        dc = DebitCard()
        dc.create_account(initial_balance=2)
        dc.charge(amount=1)
        self.assertEqual(dc.check_balance(), 1)

    def test_charge_negative(self):
        dc = DebitCard()
        dc.create_account(1)
        with self.assertRaises(AssertionError):
            dc.charge(amount=-1)


class TestDebitCardHolds(unittest.TestCase):

    def test_hold_valid(self):
        dc = DebitCard()
        dc.create_account(initial_balance=14)
        dc.hold(vendor_id=1, amount=12)
        self.assertEqual(dc.check_balance(), 2)
        self.assertEqual(dc.vendor_holds[1], 12)

    def test_hold_duplicate(self):
        dc = DebitCard()
        dc.create_account(initial_balance=14)
        dc.hold(vendor_id=1, amount=12)
        with self.assertRaises(AssertionError):
            dc.hold(vendor_id=1, amount=12)

    def test_hold_multiple(self):
        dc = DebitCard()
        dc.create_account(initial_balance=14)
        dc.hold(vendor_id=1, amount=12)
        dc.hold(vendor_id=2, amount=2)
        self.assertEqual(dc.check_balance(), 0)

    def test_settle_hold_no_vendor(self):
        dc = DebitCard()
        dc.create_account(initial_balance=14)
        with self.assertRaises(AssertionError):
            dc.settle_hold(vendor_id=None, amount=1)

    def test_settle_hold_not_active(self):
        dc = DebitCard()
        dc.create_account(initial_balance=14)
        with self.assertRaises(AssertionError):
            dc.settle_hold(vendor_id=1, amount=1)

    def test_settle_hold_valid(self):
        dc = DebitCard()
        dc.create_account(initial_balance=14)
        dc.hold(vendor_id=1, amount=12)
        dc.settle_hold(vendor_id=1, amount=5)
        self.assertEqual(dc.check_balance(), 9)
        self.assertFalse(bool(dc.vendor_holds))  # dict should be empty

    def test_settle_hold_over_charge(self):
        """balance is same as initial since insufficient funds"""
        dc = DebitCard()
        dc.create_account(initial_balance=14)
        dc.hold(vendor_id=1, amount=12)
        dc.settle_hold(vendor_id=1, amount=15)
        self.assertEqual(dc.check_balance(), 14)
        self.assertFalse(bool(dc.vendor_holds))  # dict should be empty


class TestCreditCardSystem(unittest.TestCase):

    def test_create_accounts(self):
        dcs = DebitCardSystem()
        for balance in range(10, 20):
            account_id = dcs.create_account(initial_balance=balance)
        # test one account for all functions, initial balance is 19
        # dcs.cards[account_id].balance
        dcs.charge(account_id=account_id, amount=9)
        self.assertEqual(dcs.cards[account_id].check_balance(), 10)
        dcs.hold(account_id=account_id, vendor_id=1, amount=8)
        self.assertEqual(dcs.cards[account_id].check_balance(), 2)
        dcs.settle_hold(account_id=account_id, vendor_id=1, amount=7)
        self.assertEqual(dcs.cards[account_id].check_balance(), 3)


if __name__ == '__main__':
    unittest.main()

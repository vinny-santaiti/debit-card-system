import random


class DebitCard(object):
    """ Store debit card """
    def __init__(self):
        self.account_id = None
        self._balance = 0
        self.vendor_holds = {}

    def validate_amount(self, amount):
        assert "{:.2f}".format(float(amount)), 'Currency must in format X.XX'

    def create_account(self, initial_balance):
        assert initial_balance > 0, 'balance must be greater than 0'
        self.validate_amount(initial_balance)
        self._balance = initial_balance
        self.account_id = "%0.12d" % random.randint(0, 999999999999)
        return self.account_id

    def check_balance(self, amount=0):
        self.validate_amount(amount)
        available_balance = self._balance - sum(self.vendor_holds.values())
        assert amount <= available_balance, "insufficient funds"
        return available_balance

    def charge(self, amount):
        assert amount > 0, 'amount must be greater than 0'
        self.check_balance(amount)
        self._balance -= amount

    def hold(self, vendor_id, amount):
        assert self.vendor_holds.get(vendor_id) is None, "vendor hold exists"
        self.check_balance(amount)
        self.vendor_holds[vendor_id] = amount

    def settle_hold(self, vendor_id, amount):
        assert vendor_id, "vendor_id must be valid"
        assert self.vendor_holds.get(vendor_id) is not None, "vendor hold not found"
        self.vendor_holds.pop(vendor_id, None)
        try:
            self.charge(amount)
        except AssertionError:
            pass


class DebitCardSystem(object):
    """Stores all credit cards"""

    def __init__(self):
        self.cards = {}

    def create_account(self, initial_balance):
        dc = DebitCard()
        id = dc.create_account(initial_balance)
        assert id not in self.cards, 'duplicate account id'
        self.cards[id] = dc
        return id

    def charge(self, account_id, amount):
        self.cards[account_id].charge(amount)

    def hold(self, account_id, vendor_id, amount):
        self.cards[account_id].hold(vendor_id, amount)

    def settle_hold(self, account_id, vendor_id, amount):
        self.cards[account_id].settle_hold(vendor_id, amount)


if __name__ == '__main__':
    """sample command line application that shows behavior of debit card system"""
    dcs = DebitCardSystem()
    current_id = None
    key = None
    exception_count = 0
    while exception_count < 10:
        try:
            if current_id:
                print 'current account id ', current_id, ' balance', dcs.cards[current_id].check_balance()
            print """MENU 1) see all credit cards
                2) set current card 3) create new card
                4) charge amount 5) hold amount 6) settle hold amount
                ctrl-c to quit, error count: {}""".format(exception_count)
            if bool(dcs.cards):
                key = input()
            else:
                key = 3
            if key == 1 and dcs.cards:
                print 'accounts: ', dcs.cards.keys()
            elif key == 2:
                print 'enter card id:'
                key = input()
                if key and key in dcs.cards.get(key):
                    current_id = key
            elif key == 3:
                    print 'creating new card, enter balance:'
                    key = input()
                    current_id = dcs.create_account(initial_balance=key)
            elif key == 4 and current_id:
                print 'enter charge amount:'
                key = input()
                dcs.charge(account_id=current_id, amount=key)
            elif key == 5 and current_id:
                print 'enter vendor id:'
                vendor = input()
                print 'enter hold amount:'
                amount = input()
                dcs.hold(account_id=current_id, vendor_id=vendor, amount=amount)
            elif key == 6 and current_id:
                print 'enter vendor id:'
                vendor = input()
                print 'enter settle hold amount:'
                amount = input()
                dcs.settle_hold(account_id=current_id, vendor_id=vendor, amount=amount)
        except Exception as e:
            print 'Error:', e
            exception_count += 1

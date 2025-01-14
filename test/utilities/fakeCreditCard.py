import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.creditcard import CardHandleInterface

class FakeCreditCard(CardHandleInterface):
    def __init__(self, sufficient_funds=True):
        self._sufficient_funds = sufficient_funds
        self._transaction_balance = 0

    def try_charge_amount(self, amount_in_cents: int) -> bool:
        if self._sufficient_funds:
            self._transaction_balance -= amount_in_cents
            return True
        return False

    def refund(self, amount_in_cents: int) -> None:
        self._transaction_balance += amount_in_cents

    @classmethod
    def default(cls) -> 'FakeCreditCard':
        return cls(True)

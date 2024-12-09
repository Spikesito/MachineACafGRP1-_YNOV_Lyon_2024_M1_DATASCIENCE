import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
from src.hardware.creditcard import CreditCardInterface, CardHandleInterface

class MachineACafe:
    def __init__(self, brewer: BrewerInterface, lecteur_cb: CreditCardInterface) -> None:
        lecteur_cb.register_card_detected_callback(self._credit_card_callback)
        self._brewer = brewer

    def _credit_card_callback(self, card_handle: CardHandleInterface) -> None:
        carte_debitee = card_handle.try_charge_amount(50)
        if not carte_debitee:
            return
        
        make_a_coffee_appele = self._brewer.make_a_coffee()
        if not make_a_coffee_appele:
            card_handle.refund(50)
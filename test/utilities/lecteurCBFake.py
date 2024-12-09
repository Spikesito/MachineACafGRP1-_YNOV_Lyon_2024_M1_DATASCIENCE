import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.creditcard import CreditCardInterface, CardHandleInterface

class CreditCardFake(CreditCardInterface):
    def __init__(self, has_provision=True):
        self._card_detected_callback = None
        self._has_provision = has_provision

    def simuler_cb_detectee(self):
        self._card_detected_callback(None)

    def register_card_detected_callback(self, card_detected_callback: CardHandleInterface = None) -> None:
        self._card_detected_callback = card_detected_callback
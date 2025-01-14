import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.creditcard import CreditCardInterface, CardHandleInterface

class FakeCreditCardReader(CreditCardInterface):
    def __init__(self):
        self._card_detected_callback = None

    def simulate_card_detected(self, card: CardHandleInterface) -> None:
        if self._card_detected_callback:
            self._card_detected_callback(card)

    def register_card_detected_callback(self, card_detected_callback: CardHandleInterface = None) -> None:
        self._card_detected_callback = card_detected_callback
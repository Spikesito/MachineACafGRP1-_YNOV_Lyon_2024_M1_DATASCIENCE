import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.creditcard import CreditCardInterface, CardHandleInterface

class LecteurCBFake(CreditCardInterface):
    def __init__(self):
        self._card_detected_callback = None

    def simuler_cb_detectee(self, carte: CardHandleInterface) -> None:
        self._card_detected_callback(carte)

    def register_card_detected_callback(self, card_detected_callback: CardHandleInterface = None) -> None:
        self._card_detected_callback = card_detected_callback
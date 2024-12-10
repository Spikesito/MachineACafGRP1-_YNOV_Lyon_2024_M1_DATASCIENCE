import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
from src.hardware.creditcard import CreditCardInterface, CardHandleInterface
from src.hardware.buttonpanel import ButtonCode, ButtonPanelInterface

class MachineACafe:
    def __init__(self, brewer: BrewerInterface, lecteur_cb: CreditCardInterface, button_panel: ButtonPanelInterface) -> None:
        lecteur_cb.register_card_detected_callback(self._credit_card_callback)
        button_panel.register_button_pressed_callback(self._button_pressed_callback)
        self._brewer = brewer
        self._button_panel = button_panel

    def _credit_card_callback(self, card_handle: CardHandleInterface) -> None:
        carte_debitee = card_handle.try_charge_amount(50)
        if not carte_debitee:
            return
        
        make_a_coffee_appele = self._brewer.make_a_coffee()
        if not make_a_coffee_appele:
            card_handle.refund(50)

    def _button_pressed_callback(self, button: ButtonCode):
        if button == ButtonCode.BTN_LUNGO:
            # Simule une défaillance en cas de manque d'eau
            if not self._brewer.try_pull_water():
                self._button_panel.set_lungo_warning_state(True)
            else:
                self._button_panel.set_lungo_warning_state(False)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
from src.hardware.creditcard import CreditCardInterface, CardHandleInterface
from src.hardware.buttonpanel import ButtonCode, ButtonPanelInterface
from src.hardware.cupprovider import CupProviderInterface

class MachineACafe:
    def __init__(self, brewer: BrewerInterface, lecteur_cb: CreditCardInterface, button_panel: ButtonPanelInterface, cupprovider: CupProviderInterface) -> None:
        lecteur_cb.register_card_detected_callback(self._credit_card_callback)
        button_panel.register_button_pressed_callback(self._button_pressed_callback)
        self._brewer = brewer
        self._button_panel = button_panel
        self._cup_provider = cupprovider
        self._last_button_pressed = None
        self.sugar_quantity = 0

    def _credit_card_callback(self, card_handle: CardHandleInterface) -> None:
        carte_debitee = card_handle.try_charge_amount(50)
        if not carte_debitee:
            return

        # Réinitialiser la quantité de sucre et la touillette avant la préparation
        self._brewer.reset_sugar()
        self._cup_provider.reset_stirrer()

        # Préparer le café
        make_a_coffee_appele = self._brewer.make_a_coffee()
        if not make_a_coffee_appele:
            self._button_panel.set_lungo_warning_state(True)
            card_handle.refund(50)
            return

        # Si c'est un Lungo, ajouter de l'eau
        if self._last_button_pressed == ButtonCode.BTN_LUNGO:
            if self._brewer.try_pull_water():
                self._brewer.pour_water()
            else:
                self._button_panel.set_lungo_warning_state(True)

        # Gestion du sucre et de la touillette
        if self.sugar_quantity > 0:
            self._brewer.pour_sugar(self.sugar_quantity)
            self._cup_provider.provide_stirrer()

        # Réinitialiser le sucre après préparation du café
        self.sugar_quantity = 0

    def _button_pressed_callback(self, button: ButtonCode):
        if button == ButtonCode.BTN_SUGAR_PLUS:
            self.sugar_quantity += 1
        elif button == ButtonCode.BTN_SUGAR_MINUS:
            self.sugar_quantity = max(0, self.sugar_quantity - 1)
        self._last_button_pressed = button

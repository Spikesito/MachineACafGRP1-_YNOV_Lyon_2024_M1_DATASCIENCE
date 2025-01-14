import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
from src.hardware.creditcard import CreditCardInterface, CardHandleInterface
from src.hardware.buttonpanel import ButtonCode, ButtonPanelInterface
from src.hardware.cupprovider import CupProviderInterface

class CoffeeMachine:
    def __init__(self, brewer: BrewerInterface, card_reader: CreditCardInterface, button_panel: ButtonPanelInterface, cup_provider: CupProviderInterface) -> None:
        card_reader.register_card_detected_callback(self._card_detected_callback)
        button_panel.register_button_pressed_callback(self._button_pressed_callback)
        self._brewer = brewer
        self._button_panel = button_panel
        self._cup_provider = cup_provider
        self._last_button_pressed = None
        self._sugar_quantity = 0
        self._is_lungo = False

    # Callback  quand une carte est detectée
    def _card_detected_callback(self, card_handle: CardHandleInterface) -> None:
        if not self._charge_card(card_handle):
            return

        self._prepare_for_brewing()

        if not self._brew_coffee(card_handle):
            return

        self._handle_lungo()
        self._handle_sugar_and_stirrer()

    # verifie si la carte peut être chargée
    def _charge_card(self, card_handle: CardHandleInterface) -> bool:
        if card_handle.try_charge_amount(50):
            return True
        return False

    #  reset la touillette pour la prochaine utilisation
    def _prepare_for_brewing(self) -> None:
        self._cup_provider.reset_stirrer()

    # commande la machine à café pour préparer un café
    def _brew_coffee(self, card_handle: CardHandleInterface) -> bool:
        if self._brewer.make_a_coffee():
            return True
        self._button_panel.set_lungo_warning_state(True)
        card_handle.refund(50)
        return False

    # Manage la quantité d'eau pour un lungo
    def _handle_lungo(self) -> None:
        if self._is_lungo:
            if self._brewer.try_pull_water():
                self._brewer.pour_water()
            else:
                self._button_panel.set_lungo_warning_state(True)

    # Manage l'ajout de sucre et de la touillette
    def _handle_sugar_and_stirrer(self) -> None:
        if self._sugar_quantity > 0:
            for _ in range(self._sugar_quantity):
                self._brewer.pour_sugar()         
            self._cup_provider.provide_stirrer()
        self._sugar_quantity = 0

    # Callback quand un bouton est pressé, ajuste les paramètres de la machine
    def _button_pressed_callback(self, button: ButtonCode):
        if button == ButtonCode.BTN_SUGAR_PLUS:
            self._sugar_quantity = min(5, self._sugar_quantity + 1)
        elif button == ButtonCode.BTN_SUGAR_MINUS:
            self._sugar_quantity = max(0, self._sugar_quantity - 1)
        elif button == ButtonCode.BTN_LUNGO:
            self._is_lungo = True
        self._last_button_pressed = button
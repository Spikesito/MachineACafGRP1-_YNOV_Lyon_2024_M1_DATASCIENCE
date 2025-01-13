import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
from src.hardware.creditcard import CreditCardInterface, CardHandleInterface
from src.hardware.buttonpanel import ButtonCode, ButtonPanelInterface
from src.hardware.cupprovider import CupProviderInterface

class MachineACafe:
    # Initialise la machine à café, enregistre les callbacks, etc.
    def __init__(self, brewer: BrewerInterface, lecteur_cb: CreditCardInterface, button_panel: ButtonPanelInterface, cupprovider: CupProviderInterface) -> None:
        lecteur_cb.register_card_detected_callback(self._credit_card_callback)
        button_panel.register_button_pressed_callback(self._button_pressed_callback)
        self._brewer = brewer
        self._button_panel = button_panel
        self._cup_provider = cupprovider
        self._last_button_pressed = None
        self.sugar_quantity = 0

    # Callback lors de la détection d’une carte, enclenche le processus de préparation du café
    def _credit_card_callback(self, card_handle: CardHandleInterface) -> None:
        if not self._charge_card(card_handle):
            return

        self._prepare_for_brewing()

        if not self._brew_coffee(card_handle):
            return

        self._handle_lungo()
        self._handle_sugar_and_stirrer()

    # Tente de prélever le montant nécessaire sur la carte
    def _charge_card(self, card_handle: CardHandleInterface) -> bool:
        if card_handle.try_charge_amount(50):
            return True
        return False

    # Réinitialise les paramètres de la machine pour lancer la préparation du café
    def _prepare_for_brewing(self) -> None:
        self._brewer.reset_sugar()
        self._cup_provider.reset_stirrer()

    # Lance la préparation du café, si la préparation échoue, rembourse la carte
    def _brew_coffee(self, card_handle: CardHandleInterface) -> bool:
        if self._brewer.make_a_coffee():
            return True
        self._button_panel.set_lungo_warning_state(True)
        card_handle.refund(50)
        return False

    # Gère l’ajout d’eau pour un café long
    def _handle_lungo(self) -> None:
        if self._last_button_pressed == ButtonCode.BTN_LUNGO:
            if self._brewer.try_pull_water():
                self._brewer.pour_water()
            else:
                self._button_panel.set_lungo_warning_state(True)

    # Gère l’ajout de sucre et de touillette
    def _handle_sugar_and_stirrer(self) -> None:
        if self.sugar_quantity > 0:
            self._brewer.pour_sugar(self.sugar_quantity)
            self._cup_provider.provide_stirrer()
        self.sugar_quantity = 0

    # Callback lors de l’appui sur un bouton, gère l’ajout ou la suppression de sucre
    def _button_pressed_callback(self, button: ButtonCode):
        if button == ButtonCode.BTN_SUGAR_PLUS:
            self.sugar_quantity = min(5, self.sugar_quantity + 1)
        elif button == ButtonCode.BTN_SUGAR_MINUS:
            self.sugar_quantity = max(0, self.sugar_quantity - 1)
        self._last_button_pressed = button

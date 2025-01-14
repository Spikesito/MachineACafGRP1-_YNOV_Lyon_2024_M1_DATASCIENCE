import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
from src.hardware.creditcard import CreditCardInterface
from src.coffeeMachine import CoffeeMachine
from utilities.brewerSpy import BrewerSpy
from test.utilities.brewerDefaulterFake import BrewerdefaulterFake
from test.utilities.fakeCreditCardReader import FakeCreditCardReader
from utilities.buttonPanelFake import ButtonPanelFake
from utilities.cupProviderFake import CupProviderFake

class CoffeeMachineBuilder:
    def __init__(self):
        self._lecteur_cb = FakeCreditCardReader()
        self._brewer = BrewerSpy()
        self._button_panel = ButtonPanelFake()
        self._cup_provider = CupProviderFake()
    
    def build(self) -> CoffeeMachine:
        return CoffeeMachine(self._brewer, self._lecteur_cb, self._button_panel, self._cup_provider)
    
    def with_brewer(self, brewer: BrewerInterface):
        self._brewer = brewer
        return self

    def with_credit_card_reader(self, lecteur_cb: CreditCardInterface):
        self._lecteur_cb = lecteur_cb
        return self
    
    def with_button_panel(self, button_panel: ButtonPanelFake):
        self._button_panel = button_panel
        return self
    
    def with_cup_provider(self, cup_provider: CupProviderFake):
        self._cup_provider = cup_provider
        return self
    
    def with_defective_brewer(self):
        return self.with_brewer(BrewerdefaulterFake())
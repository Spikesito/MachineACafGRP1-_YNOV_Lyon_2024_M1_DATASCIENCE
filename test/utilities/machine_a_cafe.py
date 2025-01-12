import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
from src.hardware.creditcard import CreditCardInterface
from src.machine_a_cafe import MachineACafe
from utilities.brewerSpy import BrewerSpy
from utilities.brewerDefaillantFake import BrewerDefaillantFake
from utilities.lecteurCBFake import LecteurCBFake
from utilities.buttonPanelFake import ButtonPanelFake
from utilities.CupProviderFake import CupProviderFake

class MachineACafeBuilder(MachineACafe):
    def __init__(self):
        self._lecteur_cb = LecteurCBFake()
        self._brewer = BrewerSpy()
        self._button_panel = ButtonPanelFake()
        self.cup_provider = CupProviderFake()
    
    def build(self) -> MachineACafe:
        return MachineACafe(self._brewer, self._lecteur_cb, self._button_panel, self.cup_provider)
    
    def ayant_pour_brewer(self, brewer: BrewerInterface):
        self._brewer = brewer
        return self

    def ayant_pour_lecteur_cb(self, lecteur_cb: CreditCardInterface):
        self._lecteur_cb = lecteur_cb
        return self
    
    
    def ayant_pour_button_panel(self, button_panel: ButtonPanelFake):
        self._button_panel = button_panel
        return self
    
    def ayant_pour_cup_provider(self, cup_provider: CupProviderFake):
        self.cup_provider = cup_provider
        return self
    
    def brewer_defaillant(self):
        return self.ayant_pour_brewer(BrewerDefaillantFake)
    
 
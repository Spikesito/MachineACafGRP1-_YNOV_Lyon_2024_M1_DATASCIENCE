import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
from src.hardware.creditcard import CreditCardInterface
from src.hardware.buttonpanel import ButtonPanelInterface
from src.machine_a_cafe import MachineACafe
from utilities.brewerSpy import BrewerSpy
from utilities.lecteurCBFake import LecteurCBFake

class MachineACafeBuilder(MachineACafe):
    def __init__(self):
        self._lecteur_cb = LecteurCBFake()
        self._brewer = BrewerSpy()
    
    def build(self) -> MachineACafe:
        return MachineACafe(self._brewer, self._lecteur_cb)
    
    def ayant_pour_brewer(self, brewer: BrewerInterface):
        self._brewer = brewer
        return self

    def ayant_pour_lecteur_cb(self, lecteur_cb: CreditCardInterface):
        self._lecteur_cb = lecteur_cb
        return self
    
    def ayant_pour_button_panel(self, button_panel: ButtonPanelInterface):
        return self
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.machine_a_cafe import MachineACafe
from utilities.brewer import BrewerSurveillantLesAppels
from utilities.lecteur_carte_bancaire import CreditCardSpy

class MachineACafeBuilder(MachineACafe):
    def __init__(self):
        self._lecteur_cb = CreditCardSpy()
        self._brewer = BrewerSurveillantLesAppels()
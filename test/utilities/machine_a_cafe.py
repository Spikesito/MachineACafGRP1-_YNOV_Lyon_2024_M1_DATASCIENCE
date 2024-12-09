import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.machine_a_cafe import MachineACafe
from utilities.brewerSpy import BrewerSpy
from utilities.lecteurCBSpy import CreditCardSpy

class MachineACafeBuilder(MachineACafe):
    def __init__(self):
        self._lecteur_cb = CreditCardSpy()
        self._brewer = BrewerSpy()
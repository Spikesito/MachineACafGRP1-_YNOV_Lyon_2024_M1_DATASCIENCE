import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.cupprovider import CupProviderInterface

class CupProviderFake(CupProviderInterface):
    def __init__(self):
        self._stirrer_provided = False

    def provide_stirrer(self) -> None:
        self._stirrer_provided = True

    def is_stirrer_provided(self) -> bool:
        return self._stirrer_provided
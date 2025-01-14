import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.cupprovider import CupProviderInterface

class CupProviderFake(CupProviderInterface):
    def __init__(self):
        self._provide_stirrer_called = False   

    def provide_cup(self) -> None:
        pass

    def is_cup_provided(self) -> bool:
        pass

    def is_cup_present(self) -> bool:
        pass

    def provide_stirrer(self) -> bool:
        self._provide_stirrer_called = True
        return self._provide_stirrer_called

    def was_stirrer_provided(self) -> bool:
        return self._provide_stirrer_called
    
    def reset_stirrer(self) -> None:
        self._provide_stirrer_called = False
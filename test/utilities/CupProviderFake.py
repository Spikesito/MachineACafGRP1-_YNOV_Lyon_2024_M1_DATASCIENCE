import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.cupprovider import CupProviderInterface

class CupProviderFake(CupProviderInterface):
    def __init__(self):
        self._provide_stirrer_appele = False   

    def provide_cup(self) -> None:
        pass

    def is_cup_provided(self) -> bool:
        pass

    def is_cup_present(self):
        pass

    def provide_stirrer(self) -> bool:
        self._provide_stirrer_appele = True
        return self._provide_stirrer_appele

    def provide_stirrer_appele(self) -> bool:
        return self._provide_stirrer_appele
    
    def reset_stirrer(self) -> None:
        self._provide_stirrer_appele = False  


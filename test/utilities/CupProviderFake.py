import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.cupprovider import CupProviderInterface

class CupProviderFake(CupProviderInterface):
    def __init__(self):
        self._stirrer_provided = False   #  touillette a été fournie
        self._stirrer_present = True # stock de touillettes

    def provide_cup(self) -> None:
        pass

    def is_cup_provided(self) -> bool:
        pass

    def is_cup_present(self):
        pass

    def provide_stirrer(self) -> None:
        self._stirrer_provided = True

    def is_stirrer_provided(self) -> bool:
    
        if self._stirrer_present :
            return self._stirrer_provided
        return False
    
    
    
    def is_stirrer_present(self) -> bool:
        return self._stirrer_present
    
    def reset_stirrer(self) -> None:
        self._stirrer_provided = False  


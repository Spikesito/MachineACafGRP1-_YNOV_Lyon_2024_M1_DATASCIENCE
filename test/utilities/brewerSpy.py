import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface

class BrewerSpy(BrewerInterface):
    def __init__(self):
        self._make_a_coffee_appele = False
        self.pour_sugra_appele = []

    def pour_sugar(self) -> bool:
        self.pour_sugra_appele.append(True)
        return True 
    
    def pour_chocolate(self) -> bool:
        pass

    def pour_milk(self) -> bool:
        pass

    def pour_water(self) -> bool:
        pass

    def try_pull_water(self) -> bool:
        pass

    def make_a_coffee(self) -> bool:
        self._make_a_coffee_appele = True
        return self._make_a_coffee_appele

    def make_a_coffee_appele(self) -> bool:
        _make_a_coffee_status = self._make_a_coffee_appele
        self._make_a_coffee_appele = False
        return _make_a_coffee_status
    
    def pour_sugar_appele(self) -> bool:
        pour_sugar_status = self.pour_sugra_appele
        self.pour_sugra_appele = []
        return pour_sugar_status
    
   
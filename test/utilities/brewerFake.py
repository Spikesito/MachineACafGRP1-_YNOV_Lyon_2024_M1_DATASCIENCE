import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface

class BrewerFake(BrewerInterface):
    def __init__(self, is_defaillant=False):
        self._is_defaillant = is_defaillant
        self._make_a_coffee_appele = False

    def pour_sugar(self) -> bool:
        pass

    def pour_chocolate(self) -> bool:
        pass

    def pour_milk(self) -> bool:
        pass

    def pour_water(self) -> bool:
        pass

    def try_pull_water(self) -> bool:
        pass

    def make_a_coffee(self) -> bool:
        if self._is_defaillant == False:
            self._make_a_coffee_appele = True
            return True
        return False
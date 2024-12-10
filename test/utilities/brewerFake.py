import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface

class BrewerFake(BrewerInterface):
    def __init__(self, is_defaillant=False, no_water=False):
        self._is_defaillant = is_defaillant
        self._no_water = no_water
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
        return True

    def make_a_coffee(self) -> bool:
        if not self._is_defaillant and not self._no_water:
            self._make_a_coffee_appele = True
            return True
        return False
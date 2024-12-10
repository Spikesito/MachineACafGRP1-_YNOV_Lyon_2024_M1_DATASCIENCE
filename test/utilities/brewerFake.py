import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface

class BrewerFake(BrewerInterface):
    def __init__(self, is_defaillant=False, no_more_water=False):
        self._is_defaillant = is_defaillant
        self._no_more_water = no_more_water
        self._make_a_coffee_appele = False

    def pour_sugar(self) -> bool:
        pass

    def pour_chocolate(self) -> bool:
        pass

    def pour_milk(self) -> bool:
        pass

    def pour_water(self) -> bool:
        return True

    def try_pull_water(self) -> bool:
        if self._no_more_water:
            return False
        return True

    def make_a_coffee(self) -> bool:
        if not self._is_defaillant :
            self._make_a_coffee_appele = True
            return True
        return False
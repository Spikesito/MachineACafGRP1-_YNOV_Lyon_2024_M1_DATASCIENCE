import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface
class BrewerFake(BrewerInterface):
    def __init__(self, is_defaillant=False, no_water=False, no_more_water=False, no_sugar=False):
        self._is_defaillant = is_defaillant
        self._no_sugar = no_sugar
        self._no_more_water = no_more_water
        self._no_water = no_water
        self._make_a_coffee_appele = False
        self._pour_sugra_appele = []

    def pour_sugar(self) -> bool:
        if self._no_sugar:
            self._pour_sugra_appele.append(False)
            return False
        self._pour_sugra_appele.append(True)
        return True
   
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
        if not self._is_defaillant and not self._no_water:
            self._make_a_coffee_appele = True
            return True
        return False

    def make_a_coffee_appele(self) -> bool:
        _make_a_coffee_status = self._make_a_coffee_appele
        self._make_a_coffee_appele = False
        return _make_a_coffee_status

    def pour_sugar_appele(self) -> list:
        pour_sugar_status = self._pour_sugra_appele.copy()
        self._pour_sugra_appele = []
        return pour_sugar_status 
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface

class BrewerFake(BrewerInterface):
    def __init__(self, is_defective=False, no_water=False, no_more_water=False, no_sugar=False):
        self._is_defective = is_defective
        self._no_sugar = no_sugar
        self._no_more_water = no_more_water
        self._no_water = no_water
        self._make_a_coffee_called = False
        self._pour_sugar_called = []

    def pour_sugar(self) -> bool:
        if self._no_sugar:
            self._pour_sugar_called.append(False)
            return False
        self._pour_sugar_called.append(True)
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
        if not self._is_defective and not self._no_water:
            self._make_a_coffee_called = True
            return True
        return False

    def was_make_a_coffee_called(self) -> bool:
        status = self._make_a_coffee_called
        self._make_a_coffee_called = False
        return status

    def get_pour_sugar_calls(self) -> list:
        status = self._pour_sugar_called.copy()
        self._pour_sugar_called = []
        return status
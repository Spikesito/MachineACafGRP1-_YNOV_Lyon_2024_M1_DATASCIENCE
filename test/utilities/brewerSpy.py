import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface

class BrewerSpy(BrewerInterface):
    def __init__(self):
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
        self._make_a_coffee_appele = True
        return self._make_a_coffee_appele

    def make_a_coffee_appele(self) -> bool:
        return self._make_a_coffee_appele
   
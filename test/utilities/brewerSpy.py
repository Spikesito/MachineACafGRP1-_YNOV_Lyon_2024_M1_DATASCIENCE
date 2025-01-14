import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.brewer import BrewerInterface

class BrewerSpy(BrewerInterface):
    def __init__(self):
        self._make_a_coffee_called = False
        self.pour_sugar_called = []

    def pour_sugar(self) -> bool:
        self.pour_sugar_called.append(True)
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
        self._make_a_coffee_called = True
        return self._make_a_coffee_called

    def was_make_a_coffee_called(self) -> bool:
        make_a_coffee_status = self._make_a_coffee_called
        self._make_a_coffee_called = False
        return make_a_coffee_status
    
    def get_pour_sugar_calls(self) -> list:
        pour_sugar_status = self.pour_sugar_called.copy()
        self.pour_sugar_called = []
        return pour_sugar_status
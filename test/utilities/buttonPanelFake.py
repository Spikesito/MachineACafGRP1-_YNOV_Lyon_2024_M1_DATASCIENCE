import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.buttonpanel import ButtonPanelInterface, ButtonCode

class ButtonPanelFake(ButtonPanelInterface):
    def __init__(self):
        self.lungo_warning_state = False  

    def simulate_button_press(self, button: ButtonCode) -> None:
        self._button_callback(button)

    def register_button_pressed_callback(self, button_callback):
        self._button_callback = button_callback

    def set_lungo_warning_state(self, state: bool) -> None:
        self.lungo_warning_state = state  
    
    def get_lungo_warning_state(self) -> bool:
        return self.lungo_warning_state
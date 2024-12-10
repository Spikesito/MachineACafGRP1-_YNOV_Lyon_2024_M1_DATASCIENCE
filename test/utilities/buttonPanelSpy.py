import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware.buttonpanel import ButtonPanelInterface

class ButtonPanelFake(ButtonPanelInterface):
    def __init__(self):
        pass

    def simuler_cafe_allonge(self, button):
        pass

    def register_button_pressed_callback(self, callback):
        pass

    def set_lungo_warning_state(self, state: bool) -> bool:
        return False
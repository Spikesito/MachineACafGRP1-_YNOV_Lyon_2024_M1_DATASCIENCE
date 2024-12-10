import abc

from src.hardware.buttoncode import ButtonCode

class ButtonPanelInterface(abc.ABC):
    # Enregistre un callback appelé lors de l'appui sur un bouton de la façade avant
    # @param callback prend un unique paramètre qui contiendra l'ID du bouton pressé
    @abc.abstractmethod
    def register_button_pressed_callback(self, callback: ButtonCode = None) -> None:
        pass

    # Allume ou éteint la LED informant de l'impossibilité d'avoir un allongé
    # @param state le nouvel état de la LED
    @abc.abstractmethod
    def set_lungo_warning_state(self, state: bool) -> None:
        pass
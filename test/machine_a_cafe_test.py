import unittest

from utilities.brewerSpy import BrewerSpy
from utilities.brewerFake import BrewerFake
from utilities.lecteurCBFake import LecteurCBFake
from utilities.carteFake import CarteFake
from utilities.buttonPanelFake import ButtonPanelFake
from src.hardware.buttonpanel import ButtonCode
from utilities.machine_a_cafe import MachineACafeBuilder
from test.machine_a_cafe_matcher import machine_a_cafe_matcher
from utilities.CupProviderFake import CupProviderFake

class MyTestCase(machine_a_cafe_matcher):

    def test_cas_nominal(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = LecteurCBFake()
        brewer_fake = BrewerFake()
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .build())

        # QUAND une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS un café est commandé au hardware
        self.assertCafeCommande(brewer_fake, True)
        # ET 50cts ont été débités
        self.assertCarteDebitee(carte, -50)

    def test_machine_defaillante(self):
        # ETANT DONNE une machine à café avec un brewer défaillant
        brewer_fake = BrewerFake(is_defaillant=True)
        lecteur_cb_fake = LecteurCBFake()
        button_panel = ButtonPanelFake()
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simuler_button_pressed(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la LED d'avertissement s'allume
        self.assertLedWarning(button_panel, True)    
        # ET aucun café n'est demandé au hardware
        self.assertCafeCommande(brewer_fake, False)
        # ET la carte n'a pas été débitée
        self.assertCarteDebitee(carte, 0)

    def test_manque_deau_et_led(self):
        # ETANT DONNE une machine à café manquant d'eau
        lecteur_cb_fake = LecteurCBFake()
        brewer_fake = BrewerFake(no_water=True)  # Simule le manque d'eau
        button_panel = ButtonPanelFake()
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simuler_button_pressed(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la LED d'avertissement s'allume
        self.assertLedWarning(button_panel, True)    
        # ET aucun café n'est demandé au hardware
        self.assertCafeCommande(brewer_fake, False)
        # ET aucune somme n'a été débitée
        self.assertCarteDebitee(carte, 0)

    def test_nominal_lungo(self):
        # ETANT DONNE une machine à café
        brewer_fake = BrewerFake() 
        lecteur_cb_fake = LecteurCBFake()
        button_panel = ButtonPanelFake()
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simuler_button_pressed(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la LED d'avertissement ne s'allume pas pour un café "Lungo"
        self.assertLedWarning(button_panel, False)    
        # ET la carte a été débitée
        self.assertCarteDebitee(carte, -50)

    def test_cb_manque_provision(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = LecteurCBFake()
        brewer_spy = BrewerSpy()
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_spy)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .build())

        # ET une CB n'ayant pas assez de provision
        carte = CarteFake(False)

        # QUAND cette CB est détectée
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS aucun café n'est demandé au hardware
        self.assertCafeCommande(brewer_spy, False)
        # ET la carte n'a pas été débitée
        self.assertCarteDebitee(carte, 0)

    def test_pas_de_cb(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = LecteurCBFake()
        brewer_spy = BrewerSpy()
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_spy)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .build())

        # QUAND aucune CB n'est détectée
        # ALORS aucun café n'est demandé au hardware
        self.assertCafeCommande(brewer_spy, False)

    def test_led_machine_en_manque_eau(self):
        # ETANT DONNE une machine à café avec un brewer défaillant
        brewer_fake = BrewerFake(no_more_water=True)  # Simule le manque d'eau
        lecteur_cb_fake = LecteurCBFake()
        button_panel = ButtonPanelFake()
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simuler_button_pressed(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la LED d'avertissement s'allume
        self.assertLedWarning(button_panel, True)    
        # ET 50cts ont été débités 
        self.assertCarteDebitee(carte, -50)
        


if __name__ == '__main__':
    unittest.main()

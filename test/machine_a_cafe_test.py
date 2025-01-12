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
        # ETANT DONNE une machine à café normale
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

    def test_lungo_avec_sucre_et_touillette(self):
        # ETANT DONNE une machine à café avec des touillettes disponibles
        lecteur_cb_fake = LecteurCBFake()
        brewer_spy = BrewerSpy()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()

        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_spy)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel_fake)
                          .ayant_pour_cup_provider(cup_provider_fake)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_LUNGO)

        # ET le bouton BTN_SUGAR_PLUS est pressé 3 fois
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)

        # ET que la machine est prête à faire un café
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la quantité de sucre doit être de 3
        self.assertEqual(brewer_spy.get_sugar_quantity(), 3)

        # ET une touillette doit avoir été fournie
        self.assertTrue(cup_provider_fake.is_stirrer_provided())

        # ALORS la LED d'avertissement ne s'allume pas
        self.assertLedWarning(button_panel_fake, False)
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

    def test_cafe_sans_sucre_pas_de_touillette(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = LecteurCBFake()
        brewer_fake = BrewerFake()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()
        
        machine_a_cafe = (MachineACafeBuilder()
                        .ayant_pour_brewer(brewer_fake)
                        .ayant_pour_lecteur_cb(lecteur_cb_fake)
                        .ayant_pour_button_panel(button_panel_fake)
                        .ayant_pour_cup_provider(cup_provider_fake)
                        .build())

        # QUAND une CB est détectée (sans appuyer sur le bouton sucre)
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS aucun sucre ne doit être ajouté
        self.assertCafeCommande(brewer_fake, True)
        # ET aucune touillette ne doit être fournie
        self.assertFalse(cup_provider_fake.is_stirrer_provided())
        # ET la carte a été débitée
        self.assertCarteDebitee(carte, -50)

    def test_ajout_sucre(self):
        lecteur_cb_fake = LecteurCBFake()
        brewer_spy = BrewerSpy()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()

        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_spy)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel_fake)
                          .ayant_pour_cup_provider(cup_provider_fake)
                          .build())

        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)

        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        self.assertEqual(brewer_spy.get_sugar_quantity(), 2)
        self.assertTrue(cup_provider_fake.is_stirrer_provided())

    def test_reduction_sucre(self):
        lecteur_cb_fake = LecteurCBFake()
        brewer_spy = BrewerSpy()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()

        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_spy)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel_fake)
                          .ayant_pour_cup_provider(cup_provider_fake)
                          .build())

        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_MINUS)

        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        self.assertEqual(brewer_spy.get_sugar_quantity(), 1)
        self.assertTrue(cup_provider_fake.is_stirrer_provided())

    def test_sucre_cycle_reinitialisation(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = LecteurCBFake()
        brewer_fake = BrewerFake()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()
        
        machine_a_cafe = (MachineACafeBuilder()
                        .ayant_pour_brewer(brewer_fake)
                        .ayant_pour_lecteur_cb(lecteur_cb_fake)
                        .ayant_pour_button_panel(button_panel_fake)
                        .ayant_pour_cup_provider(cup_provider_fake)
                        .build())

        # QUAND le bouton sucre est pressé 2 fois
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        
        # ET une CB est détectée pour un premier café
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS le café doit être préparé
        self.assertCafeCommande(brewer_fake, True)
        # ET une touillette doit être fournie car il y a du sucre
        self.assertTrue(cup_provider_fake.is_stirrer_provided())
        
        
        # QUAND une nouvelle CB est détectée sans appuyer sur le bouton sucre
        carte2 = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte2)



        # ALORS le café doit être préparé
        self.assertCafeCommande(brewer_fake, True)
        self.assertEqual(brewer_fake.get_sugar_quantity(), 0)
        # ET aucune touillette ne doit être fournie car pas de sucre
        self.assertFalse(cup_provider_fake.is_stirrer_provided())

        


if __name__ == '__main__':
    unittest.main()

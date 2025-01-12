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


class MyTestCaseSucre(machine_a_cafe_matcher):

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

        # QUAND une CB est détectée pour un café sans sucre
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS aucun sucre ne doit être ajouté
        self.assertCafeCommande(brewer_fake, True)
        self.assertEqual(brewer_fake.get_sugar_quantity(), 0)
        # ET aucune touillette ne doit être fournie
        self.assertFalse(cup_provider_fake.is_stirrer_provided())
        # ET la carte a été débitée
        self.assertCarteDebitee(carte, -50)

    def test_ajout_sucre_avec_touillette(self):
        # ETANT DONNE une machine à café
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

        # Ajouter du sucre
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)

        # Détecter la CB
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # Vérifie que la quantité de sucre est de 1
        self.assertEqual(brewer_spy.get_sugar_quantity(), 1)
        # La touillette est fournie
        self.assertTrue(cup_provider_fake.is_stirrer_provided())
        # Vérifie le débit de la carte
        self.assertCarteDebitee(carte, -50)

    def test_reduction_sucre(self):
        # ETANT DONNE une machine à café
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
        # Ajout de  1 sucre
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_MINUS)

        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        #  ALORS un café est commandé au hardware
        self.assertCafeCommande(brewer_spy, True)
        # ET  un sucre ne doit être ajouté
        self.assertEqual(brewer_spy.get_sugar_quantity(), 1)
        # ET une touillette doit être fournie
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

        # Ajouter 2 sucres pour le premier café
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)

        # QUAND cette CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS un café est commandé au hardware
        self.assertCafeCommande(brewer_fake, True)
        # ET deux sucres doivent être ajoutés	
        self.assertEqual(brewer_fake.get_sugar_quantity(), 2)
        # ET une touillette doit être fournie
        self.assertTrue(cup_provider_fake.is_stirrer_provided())
        # ET 50cts ont été débités
        self.assertCarteDebitee(carte, -50)
        
    
        
        # Détecter une nouvelle CB pour un café sans sucre
        carte2 = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte2)

        # ALORS un café est commandé au hardware	
        self.assertCafeCommande(brewer_fake, True)
        # ET aucun sucre ne doit être ajouté
        self.assertEqual(brewer_fake.get_sugar_quantity(), 0)
        # ET aucune touillette ne doit être fournie
        self.assertFalse(cup_provider_fake.is_stirrer_provided())
        # ET 50cts ont été débités
        self.assertCarteDebitee(carte, -50)

    def test_sucre_cycle_avec_sucre_reduit_à_zero(self):
        # ETANT DONNE une machine à café
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
        # retirer 2 sucres pour voir le sucre reste à 0
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_MINUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_MINUS)

        # QUAND une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS un café est commandé au hardware
        self.assertCafeCommande(brewer_spy, True)

        # ET aucun sucre ne doit être ajouté
        self.assertEqual(brewer_spy.get_sugar_quantity(), 0)
        # ET aucune touillette ne doit être fournie
        self.assertFalse(cup_provider_fake.is_stirrer_provided())

        # Vérifie le débit de la carte
        self.assertCarteDebitee(carte, -50)

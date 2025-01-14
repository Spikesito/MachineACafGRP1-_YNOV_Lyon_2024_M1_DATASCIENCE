import unittest

from utilities.brewerSpy import BrewerSpy
from utilities.brewerFake import BrewerFake
from utilities.lecteurCBFake import LecteurCBFake
from utilities.carteFake import CarteFake
from utilities.buttonPanelFake import ButtonPanelFake
from src.hardware.buttonpanel import ButtonCode
from utilities.machine_a_cafe import MachineACafeBuilder
from machine_a_cafe_matcher import machine_a_cafe_matcher
from utilities.CupProviderFake import CupProviderFake


class TestMachineCafeSucre(machine_a_cafe_matcher):

    def test_cafe_commande_sans_touillette(self):
        # ÉTANT DONNÉ une machine à café
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

        # QUAND une carte bancaire est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS un café est commandé sans sucre
        self.assertCafeCommande(brewer_fake, True)
        self.assertSansSucre(brewer_fake)
        # ET aucune touillette ne doit être fournie
        self.assertStirrerProvided(cup_provider_fake, False)
        # ET la carte a été débitée
        self.assertCarteDebitee(carte, -50)

    def test_ajout_sucre_avec_touillette(self):
        # ÉTANT DONNÉ une machine à café
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

        # Détecter la carte
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # Vérifie que la quantité de sucre est bien délivrée
        self.assertPourSugar(brewer_spy, reussite=True)
        # La touillette est fournie
        self.assertStirrerProvided(cup_provider_fake, True)
        # Vérifie le débit de la carte
        self.assertCarteDebitee(carte, -50)

    def test_reduction_sucre(self):
        # ÉTANT DONNÉ une machine à café
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

        # Ajout de 1 sucre
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_MINUS)

        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS un café est commandé au hardware
        self.assertCafeCommande(brewer_spy, True)
        # ET vérifie que la quantité de sucre est bien délivrée
        self.assertPourSugar(brewer_spy, True)
        # ET une touillette doit être fournie
        self.assertStirrerProvided(cup_provider_fake, True)

    def test_sucre_cycle_reinitialisation(self):
        # ÉTANT DONNÉ une machine à café
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

        # QUAND cette carte est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS un café est commandé au hardware
        self.assertCafeCommande(brewer_fake, True)
        # ET vérifie que la quantité de sucre est bien délivrée
        self.assertPourSugar(brewer_fake, True)
        # ET une touillette doit être fournie
        self.assertStirrerProvided(cup_provider_fake, True)
        # ET 50cts ont été débités
        self.assertCarteDebitee(carte, -50)

        # Détecter une nouvelle carte pour un café sans sucre
        carte2 = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte2)

        # ALORS un café est commandé au hardware
        self.assertCafeCommande(brewer_fake, True)
        # ET vérifie qu'aucun sucre n'est délivré
        self.assertSansSucre(brewer_fake)
        # ET aucune touillette ne doit être fournie
        self.assertStirrerProvided(cup_provider_fake, False)
        # ET 50cts ont été débités
        self.assertCarteDebitee(carte2, -50)

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
        
        # retirer 2 sucres à une quantité initial de 0 sucre
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_MINUS)
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_MINUS)

        # QUAND une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS un café est commandé au hardware
        self.assertCafeCommande(brewer_spy, True)

        # ET aucun sucre ne doit être ajouté
        self.assertSansSucre(brewer_spy)
        # ET aucune touillette ne doit être fournie
        self.assertStirrerProvided(cup_provider_fake, False)

        # Vérifie le débit de la carte
        self.assertCarteDebitee(carte, -50)
    
    def test_machine_defaillante_et_sucre_non_distribué(self):
        # ETANT DONNE une machine à café avec un brewer défaillant
        brewer_fake = BrewerFake(no_sugar=True)
        lecteur_cb_fake = LecteurCBFake()
        button_panel_fake = ButtonPanelFake()

        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel_fake)
                          .build())

        # Ajouter 1 sucres pour le premier café
        button_panel_fake.simuler_button_pressed(ButtonCode.BTN_SUGAR_PLUS)

        # ET une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la LED d'avertissement s'allume
        self.assertLedWarning(button_panel_fake, True)   
        # ET aucun café n'est demandé au hardware
        self.assertCafeCommande(brewer_fake, False)
        # ET la carte n'a pas été débitée
        self.assertCarteDebitee(carte, 0)
        # ET aucun sucre n'est distribué
        self.assertPourSugar(brewer_fake, echec=True)

if __name__ == '__main__':
    unittest.main()
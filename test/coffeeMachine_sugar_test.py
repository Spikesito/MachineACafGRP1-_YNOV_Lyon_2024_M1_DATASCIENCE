import unittest

from utilities.brewerSpy import BrewerSpy
from utilities.brewerFake import BrewerFake
from utilities.fakeCreditCardReader import FakeCreditCardReader
from test.utilities.fakeCreditCard import FakeCreditCard
from utilities.buttonPanelFake import ButtonPanelFake
from src.hardware.buttonpanel import ButtonCode
from test.utilities.coffeeMachine import CoffeeMachineBuilder
from test.coffeeMachineMatcher import CoffeeMachineMatcher
from utilities.cupProviderFake import CupProviderFake


class TestMachineCafeSucre(CoffeeMachineMatcher):

    def test_cafe_commande_sans_touillette(self):
        # ÉTANT DONNÉ une machine à café
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_fake = BrewerFake()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()

        machine_a_cafe = (CoffeeMachineBuilder()
                            .with_brewer(brewer_fake)
                            .with_credit_card_reader(lecteur_cb_fake)
                            .with_button_panel(button_panel_fake)
                            .with_cup_provider(cup_provider_fake)
                            .build())

        # QUAND une carte bancaire est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS un café est commandé sans sucre
        self.assert_coffee_ordered(brewer_fake, True)
        self.assert_no_sugar(brewer_fake)
        # ET aucune touillette ne doit être fournie
        self.assert_stirrer_provided(cup_provider_fake, False)
        # ET la carte a été débitée
        self.assert_card_debited(carte, -50)

    def test_ajout_sucre_avec_touillette(self):
        # ÉTANT DONNÉ une machine à café
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_spy = BrewerSpy()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()

        machine_a_cafe = (CoffeeMachineBuilder()
                            .with_brewer(brewer_spy)
                            .with_credit_card_reader(lecteur_cb_fake)
                            .with_button_panel(button_panel_fake)
                            .with_cup_provider(cup_provider_fake)
                            .build())

        # Ajouter du sucre
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_PLUS)

        # Détecter la carte
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # Vérifie que la quantité de sucre est bien délivrée
        self.assert_pour_sugar(brewer_spy, success=True)
        # La touillette est fournie
        self.assert_stirrer_provided(cup_provider_fake, True)
        # Vérifie le débit de la carte
        self.assert_card_debited(carte, -50)

    def test_reduction_sucre(self):
        # ÉTANT DONNÉ une machine à café
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_spy = BrewerSpy()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()

        machine_a_cafe = (CoffeeMachineBuilder()
                            .with_brewer(brewer_spy)
                            .with_credit_card_reader(lecteur_cb_fake)
                            .with_button_panel(button_panel_fake)
                            .with_cup_provider(cup_provider_fake)
                            .build())

        # Ajout de 1 sucre
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_MINUS)

        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS un café est commandé au hardware
        self.assert_coffee_ordered(brewer_spy, True)
        # ET vérifie que la quantité de sucre est bien délivrée
        self.assert_pour_sugar(brewer_spy, True)
        # ET une touillette doit être fournie
        self.assert_stirrer_provided(cup_provider_fake, True)

    def test_sucre_cycle_reinitialisation(self):
        # ÉTANT DONNÉ une machine à café
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_fake = BrewerFake()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()

        machine_a_cafe = (CoffeeMachineBuilder()
                            .with_brewer(brewer_fake)
                            .with_credit_card_reader(lecteur_cb_fake)
                            .with_button_panel(button_panel_fake)
                            .with_cup_provider(cup_provider_fake)
                            .build())

        # Ajouter 2 sucres pour le premier café
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_PLUS)
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_PLUS)

        # QUAND cette carte est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS un café est commandé au hardware
        self.assert_coffee_ordered(brewer_fake, True)
        # ET vérifie que la quantité de sucre est bien délivrée
        self.assert_pour_sugar(brewer_fake, True)
        # ET une touillette doit être fournie
        self.assert_stirrer_provided(cup_provider_fake, True)
        # ET 50cts ont été débités
        self.assert_card_debited(carte, -50)

        # Détecter une nouvelle carte pour un café sans sucre
        carte2 = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte2)

        # ALORS un café est commandé au hardware
        self.assert_coffee_ordered(brewer_fake, True)
        # ET vérifie qu'aucun sucre n'est délivré
        self.assert_no_sugar(brewer_fake)
        # ET aucune touillette ne doit être fournie
        self.assert_stirrer_provided(cup_provider_fake, False)
        # ET 50cts ont été débités
        self.assert_card_debited(carte2, -50)

    def test_sucre_cycle_avec_sucre_reduit_à_zero(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_spy = BrewerSpy()
        button_panel_fake = ButtonPanelFake()
        cup_provider_fake = CupProviderFake()

        machine_a_cafe = (CoffeeMachineBuilder()
                            .with_brewer(brewer_spy)
                            .with_credit_card_reader(lecteur_cb_fake)
                            .with_button_panel(button_panel_fake)
                            .with_cup_provider(cup_provider_fake)
                            .build())
        
        # retirer 2 sucres à une quantité initial de 0 sucre
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_MINUS)
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_MINUS)

        # QUAND une CB est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS un café est commandé au hardware
        self.assert_coffee_ordered(brewer_spy, True)

        # ET aucun sucre ne doit être ajouté
        self.assert_no_sugar(brewer_spy)
        # ET aucune touillette ne doit être fournie
        self.assert_stirrer_provided(cup_provider_fake, False)

        # Vérifie le débit de la carte
        self.assert_card_debited(carte, -50)
    
    def test_machine_defaillante_et_sucre_non_distribué(self):
        # ETANT DONNE une machine à café avec un brewer défaillant
        brewer_fake = BrewerFake(no_sugar=True)
        lecteur_cb_fake = FakeCreditCardReader()
        button_panel_fake = ButtonPanelFake()

        machine_a_cafe = (CoffeeMachineBuilder()
                          .with_brewer(brewer_fake)
                          .with_credit_card_reader(lecteur_cb_fake)
                          .with_button_panel(button_panel_fake)
                          .build())

        # Ajouter 1 sucres pour le premier café
        button_panel_fake.simulate_button_press(ButtonCode.BTN_SUGAR_PLUS)

        # ET une CB est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)
   
        # ET un café est demandé au hardware
        self.assert_coffee_ordered(brewer_fake, True)
        # ET la carte a été débitée
        self.assert_card_debited(carte, -50)
        # ET aucun sucre n'est distribué
        self.assert_pour_sugar(brewer_fake, failure=True)

if __name__ == '__main__':
    unittest.main()
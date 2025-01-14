import unittest

from utilities.brewerSpy import BrewerSpy
from utilities.brewerFake import BrewerFake
from test.utilities.fakeCreditCardReader import FakeCreditCardReader
from test.utilities.fakeCreditCard import FakeCreditCard
from utilities.buttonPanelFake import ButtonPanelFake
from src.hardware.buttonpanel import ButtonCode
from test.utilities.coffeeMachine import CoffeeMachineBuilder
from test.coffeeMachineMatcher import CoffeeMachineMatcher

class MyTestCase(CoffeeMachineMatcher):

    def test_cas_nominal(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_fake = BrewerFake()
        coffeeMachine = (CoffeeMachineBuilder()
                          .with_brewer(brewer_fake)
                          .with_credit_card_reader(lecteur_cb_fake)
                          .build())

        # QUAND une CB est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS un café est commandé au hardware
        self.assert_coffee_ordered(brewer_fake, True)
        # ET 50cts ont été débités
        self.assert_card_debited(carte, -50)

    def test_machine_defaillante(self):
        # ETANT DONNE une machine à café avec un brewer défaillant
        brewer_fake = BrewerFake(is_defective=True)
        lecteur_cb_fake = FakeCreditCardReader()
        button_panel = ButtonPanelFake()
        coffeeMachine = (CoffeeMachineBuilder()
                          .with_brewer(brewer_fake)
                          .with_credit_card_reader(lecteur_cb_fake)
                          .with_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simulate_button_press(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS la LED d'avertissement s'allume
        self.assert_led_warning(button_panel, True)    
        # ET aucun café n'est demandé au hardware
        self.assert_coffee_ordered(brewer_fake, False)
        # ET la carte n'a pas été débitée
        self.assert_card_debited(carte, 0)

    def test_manque_deau_et_led(self):
        # ETANT DONNE une machine à café manquant d'eau
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_fake = BrewerFake(no_water=True)  # Simule le manque d'eau
        button_panel = ButtonPanelFake()
        coffeeMachine = (CoffeeMachineBuilder()
                          .with_brewer(brewer_fake)
                          .with_credit_card_reader(lecteur_cb_fake)
                          .with_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simulate_button_press(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS la LED d'avertissement s'allume
        self.assert_led_warning(button_panel, True)    
        # ET aucun café n'est demandé au hardware
        self.assert_coffee_ordered(brewer_fake, False)
        # ET aucune somme n'a été débitée
        self.assert_card_debited(carte, 0)

    def test_nominal_lungo(self):
        # ETANT DONNE une machine à café
        brewer_fake = BrewerFake() 
        lecteur_cb_fake = FakeCreditCardReader()
        button_panel = ButtonPanelFake()
        coffeeMachine = (CoffeeMachineBuilder()
                          .with_brewer(brewer_fake)
                          .with_credit_card_reader(lecteur_cb_fake)
                          .with_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simulate_button_press(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS la LED d'avertissement ne s'allume pas pour un café "Lungo"
        self.assert_led_warning(button_panel, False)    
        # ET la carte a été débitée
        self.assert_card_debited(carte, -50)

    def test_cb_manque_provision(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_spy = BrewerSpy()
        coffeeMachine = (CoffeeMachineBuilder()
                          .with_brewer(brewer_spy)
                          .with_credit_card_reader(lecteur_cb_fake)
                          .build())

        # ET une CB n'ayant pas assez de provision
        carte = FakeCreditCard(False)

        # QUAND cette CB est détectée
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS aucun café n'est demandé au hardware
        self.assert_coffee_ordered(brewer_spy, False)
        # ET la carte n'a pas été débitée
        self.assert_card_debited(carte, 0)

    def test_pas_de_cb(self):
        # ETANT DONNE une machine à café
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_spy = BrewerSpy()
        coffeeMachine = (CoffeeMachineBuilder()
                          .with_brewer(brewer_spy)
                          .with_credit_card_reader(lecteur_cb_fake)
                          .build())

        # QUAND aucune CB n'est détectée
        # ALORS aucun café n'est demandé au hardware
        self.assert_coffee_ordered(brewer_spy, False)

    def test_led_machine_en_manque_eau(self):
        # ETANT DONNE une machine à café avec un brewer défaillant
        brewer_fake = BrewerFake(no_more_water=True)  # Simule le manque d'eau
        lecteur_cb_fake = FakeCreditCardReader()
        button_panel = ButtonPanelFake()
        coffeeMachine = (CoffeeMachineBuilder()
                          .with_brewer(brewer_fake)
                          .with_credit_card_reader(lecteur_cb_fake)
                          .with_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simulate_button_press(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS la LED d'avertissement s'allume
        self.assert_led_warning(button_panel, True)    
        # ET 50cts ont été débités 
        self.assert_card_debited(carte, -50)

    def test_couler_cafe_long_et_plus_d_eau_pour_expresso(self):
        # ETANT DONNE une machine à café avec de l'eau initialement
        lecteur_cb_fake = FakeCreditCardReader()
        brewer_fake = BrewerFake()
        button_panel = ButtonPanelFake()
        coffeeMachine = (CoffeeMachineBuilder()
                        .with_brewer(brewer_fake)
                        .with_credit_card_reader(lecteur_cb_fake)
                        .with_button_panel(button_panel)
                        .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simulate_button_press(ButtonCode.BTN_LUNGO)
        # ET une CB est détectée
        carte = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte)

        # ALORS un café est commandé au hardware
        self.assert_coffee_ordered(brewer_fake, True)
        # ET 50cts ont été débités
        self.assert_card_debited(carte, -50)

        # ET la machine est maintenant à court d'eau
        brewer_fake._no_water = True 

        # QUAND une carte est détectée 
        carte2 = FakeCreditCard.default()
        lecteur_cb_fake.simulate_card_detected(carte2)

        # ALORS aucun café ne doit être préparé
        self.assert_coffee_ordered(brewer_fake, False)
        # ET la LED d'avertissement s'allume
        self.assert_led_warning(button_panel, True)
        # ET la carte n'est pas débitée
        self.assert_card_debited(carte2, 0)
        
if __name__ == '__main__':
    unittest.main()

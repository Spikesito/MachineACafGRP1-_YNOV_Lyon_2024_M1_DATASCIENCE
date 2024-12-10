import unittest

from utilities.brewerSpy import BrewerSpy
from utilities.brewerFake import BrewerFake
from utilities.lecteurCBFake import LecteurCBFake
from utilities.carteFake import CarteFake
from utilities.buttonPanelFake import ButtonPanelFake
from src.hardware.buttonpanel import ButtonCode
from utilities.machine_a_cafe import MachineACafeBuilder

class MyTestCase(unittest.TestCase):

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
        self.assertTrue(brewer_fake.make_a_coffee())

        # ET 50cts ont été débités (pas encore)
        self.assertEqual(-50, carte._somme_operations)
    
    def test_defaillant(self):
        # ETANT DONNE une machine à café manquant de café
        lecteur_cb_fake = LecteurCBFake()
        brewer_fake = BrewerFake(is_defaillant=True)
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .build())

        # QUAND une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS aucun café n'est demandé au hardware
        self.assertFalse(brewer_fake.make_a_coffee())

        # ET la carte n'a pas été débitée
        self.assertEqual(0, carte._somme_operations)
    

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
        self.assertFalse(brewer_spy.make_a_coffee())
        # ET la carte n'a pas été débitée
        self.assertEqual(0, carte._somme_operations)

    def test_manque_deau(self):
        # ETANT DONNE une machine à café manquant d'eau
        lecteur_cb_fake = LecteurCBFake()
        brewer_fake = BrewerFake(no_water=True)
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .build())
        
        # QUAND une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS aucun café n'est demandé au hardware
        self.assertFalse(brewer_fake.make_a_coffee())
        # ET aucune somme n'a été débitée
        self.assertEqual(0, carte._somme_operations)
        
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
        self.assertFalse(brewer_spy.make_a_coffee())

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
        button_panel.simuler_button_pressed(ButtonCode.BTN_LUNGO) # 0 est le code du café allongé
        # ET une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la LED d'avertissement s'allume
        self.assertTrue(button_panel.get_lungo_warning_state()) # False par défaut car la LED n'est pas encore rouge
        # ET 50cts ont été débités (pas encore)
        self.assertEqual(-50, carte._somme_operations)

    def test_led_machine_en_erreur_coffee(self):
        # ETANT DONNE une machine à café avec un brewer défaillant
        brewer_fake = BrewerFake(is_defaillant=True)  # Simule problème cafe
        lecteur_cb_fake = LecteurCBFake()
        button_panel = ButtonPanelFake()
        machine_a_cafe = (MachineACafeBuilder()
                          .ayant_pour_brewer(brewer_fake)
                          .ayant_pour_lecteur_cb(lecteur_cb_fake)
                          .ayant_pour_button_panel(button_panel)
                          .build())

        # QUAND le bouton BTN_LUNGO est pressé
        button_panel.simuler_button_pressed(ButtonCode.BTN_LUNGO) # 0 est le code du café allongé
        # ET une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la LED d'avertissement s'allume
        self.assertTrue(button_panel.get_lungo_warning_state()) # False par défaut car la LED n'est pas encore rouge    
        # ET la carte n'a pas été débitée
        self.assertEqual(0, carte._somme_operations)
    
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
        button_panel.simuler_button_pressed(ButtonCode.BTN_LUNGO) # 0 est le code du café allongé
        # ET une CB est détectée
        carte = CarteFake.default()
        lecteur_cb_fake.simuler_cb_detectee(carte)

        # ALORS la LED d'avertissement ne s'allume pas
        self.assertFalse(button_panel.get_lungo_warning_state()) # False par défaut car la LED n'est pas encore rouge    
        # ET la carte a été débitée
        self.assertEqual(-50, carte._somme_operations)



if __name__ == '__main__':
    unittest.main()

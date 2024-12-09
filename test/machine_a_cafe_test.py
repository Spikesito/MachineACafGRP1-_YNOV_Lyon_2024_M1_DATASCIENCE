import unittest

from utilities.brewerSpy import BrewerSpy
from utilities.brewerFake import BrewerFake
from utilities.lecteurCBSpy import CreditCardSpy
from utilities.lecteurCBFake import CreditCardFake
from utilities.machine_a_cafe import MachineACafe

class MyTestCase(unittest.TestCase):

    def test_cas_nominal(self):
        # ETANT DONNE une machine à café
        lecteur_cb = CreditCardSpy()
        brewer = BrewerSpy()
        machine_a_cafe = MachineACafe(brewer, lecteur_cb)

        # QUAND une CB est détectée
        lecteur_cb.simuler_cb_detectee()

        # ALORS un café est commandé au hardware
        # ET 50cts ont été débités (pas encore)
        self.assertTrue(brewer.make_a_coffee_appele())
    
    def test_cafe_manquant(self):
        # ETANT DONNE une machine à café manquant de café
        lecteur_cb = CreditCardSpy()
        brewer_fake = BrewerFake(has_coffee=False)
        machine_a_cafe = MachineACafe(brewer_fake, lecteur_cb)

        # QUAND une CB est détectée
        lecteur_cb.simuler_cb_detectee()

        # ALORS aucun café n'est demandé au hardware
        self.assertFalse(brewer_fake.make_a_coffee())
    
    def test_cb_manque_provision(self):
        # ETANT DONNE une machine à café
        # ET une CB n'ayant pas assez de provision
        lecteur_cb_fake = CreditCardFake(has_provision=False)
        brewer_fake = BrewerFake()
        machine_a_cafe = MachineACafe(brewer_fake, lecteur_cb_fake)

        # QUAND cette CB est détectée
        lecteur_cb_fake.simuler_cb_detectee()

        # ALORS aucun café n'est demandé au hardware
        self.assertFalse(brewer_fake.make_a_coffee())

        # ETANT DONNE une machine à café manquant d'eau
        # QUAND une CB est détectée
        # ALORS aucun café n'est demandé au hardware
        # ET aucune somme n'a été débitée
        
        # ETANT DONNE une machine à café
        # QUAND aucune CB n'est détectée
        # ALORS aucun café n'est demandé au hardware


if __name__ == '__main__':
    unittest.main()

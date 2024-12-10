import unittest

from utilities.brewerSpy import BrewerSpy
from utilities.brewerFake import BrewerFake
from utilities.lecteurCBFake import LecteurCBFake
from utilities.carteFake import CarteFake
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
        
    # ETANT DONNE une machine à café
    # QUAND aucune CB n'est détectée
    # ALORS aucun café n'est demandé au hardware


if __name__ == '__main__':
    unittest.main()

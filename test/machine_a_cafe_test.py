import unittest

from utilities.brewer import BrewerSurveillantLesAppels
from utilities.machine_a_cafe import MachineACafe
from utilities.lecteur_carte_bancaire import CreditCardSpy

class MyTestCase(unittest.TestCase):

    def test_cas_nominal(self):
        # ETANT DONNE une machine à café
        lecteur_cb = CreditCardSpy()
        brewer = BrewerSurveillantLesAppels()
        machine_a_cafe = MachineACafe(brewer, lecteur_cb)

        # QUAND une CB est détectée
        lecteur_cb.simuler_cb_detectee()

        # ALORS un café est commandé au hardware
        # ET 50cts ont été débités (pas encore)
        self.assertTrue(brewer.make_a_coffee_appele())
    
    # ETANT DONNE une machine à café manquant de café
    # QUAND une CB est détectée
    # ALORS aucun café n'est demandé au hardware
    # ET aucune somme n'a été débitée
    
    # ETANT DONNE une machine à café
    # ET une CB n'ayant pas assez de provision
    # QUAND cette CB est détectée
    # ALORS aucun café n'est demandé au hardware
    
    # ETANT DONNE une machine à café manquant d'eau
    # QUAND une CB est détectée
    # ALORS aucun café n'est demandé au hardware
    # ET aucune somme n'a été débitée
    
    # ETANT DONNE une machine à café
    # QUAND aucune CB n'est détectée
    # ALORS aucun café n'est demandé au hardware


if __name__ == '__main__':
    unittest.main()

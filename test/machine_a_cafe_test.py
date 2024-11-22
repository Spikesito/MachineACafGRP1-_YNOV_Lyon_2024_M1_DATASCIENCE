import unittest

from utilities.brewer import Brewer
from utilities.machine_a_cafe import MachineACafe
from utilities.lecteur_carte_bancaire import LecteurCB

class MyTestCase(unittest.TestCase):

    def test_cas_nominal(self):
        # ETANT DONNE une machine à café
        lecteur_cb = LecteurCB()
        brewer = Brewer()
        machine_a_cafe = MachineACafe()

        # QUAND une CB est détectée
        lecteur_cb.simuler_cb_detectee()

        # ALORS un café est commandé au hardware
        # ET 50cts ont été débités (pas encore)
        self.assertTrue(brewer.commande_cafe_appele())
    
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

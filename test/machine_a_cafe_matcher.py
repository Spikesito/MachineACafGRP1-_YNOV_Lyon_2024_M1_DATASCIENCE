import unittest

class machine_a_cafe_matcher(unittest.TestCase):
    def assertCarteDebitee(self, carte, montant_attendu):
        self.assertEqual(
            montant_attendu, carte._somme_operations,
            f"La carte n'a pas été débitée correctement. Attendu: {montant_attendu}, Trouvé: {carte._somme_operations}"
        )

    def assertCafeCommande(self, brewer, attendu):
        result = brewer.make_a_coffee_appele()
        self.assertEqual(
            attendu, result,
            f"Commande de café incorrecte. Attendu: {attendu}, Trouvé: {result}"
    )

    def assertLedWarning(self, button_panel, attendu):
        self.assertEqual(
            attendu, button_panel.get_lungo_warning_state(),
            f"État de la LED incorrect. Attendu: {attendu}, Trouvé: {button_panel.get_lungo_warning_state()}"
        )

    def assertButtonPressed(self, button_panel, button_code, pressed=True):
        self.assertEqual(
            pressed, button_panel.is_button_pressed(button_code),
            f"État du bouton {button_code} incorrect. Attendu: {pressed}, Trouvé: {not pressed}"
        )

    def assertMachineState(self, brewer, no_water=False, is_defaillant=False):
        self.assertEqual(
            no_water, brewer.no_more_water,
            f"Problème de manque d'eau incorrect. Attendu: {no_water}, Trouvé: {brewer.no_more_water}"
        )
        self.assertEqual(
            is_defaillant, brewer.is_defaillant,
            f"Problème de défaillance du hardware incorrect. Attendu: {is_defaillant}, Trouvé: {brewer.is_defaillant}"
        )

    def assertStirrerProvided(self, cup_provider, attendu):
        self.assertEqual(
            attendu, cup_provider.provide_stirrer_appele(),
            f"Présence de touillette incorrecte. Attendu: {attendu}, Trouvé: {cup_provider.provide_stirrer_appele()}"
        )

    def assertPourSugar(self, brewer, reussite=False, echec=False):
        self.assertEqual(
            reussite, all(brewer.pour_sugar_appele()),
            f"Quantité de sucre incorrecte. Attendu: {reussite}, Trouvé: {brewer.pour_sugar_appele()}"
        )

        self.assertEqual(
            echec, not all(brewer.pour_sugar_appele()),
            f"Quantité de sucre incorrecte. Attendu: {not echec}, Trouvé: {brewer.pour_sugar_appele()}"
        )
    
    def assertSansSucre(self, brewer):
        self.assertEqual(
            0, len(brewer.pour_sugar_appele()),
            f"Quantité de sucre incorrecte. Attendu: 0, Trouvé: {brewer.pour_sugar_appele()}"
        )

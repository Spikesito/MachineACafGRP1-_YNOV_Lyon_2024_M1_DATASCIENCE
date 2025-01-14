import unittest

class CoffeeMachineMatcher(unittest.TestCase):
    def assert_card_debited(self, card, expected_amount):
        self.assertEqual(
            expected_amount, card._transaction_balance,
            f"La carte n'a pas été débitée correctement. Attendu: {expected_amount}, Trouvé: {card._transaction_balance}"
        )

    def assert_coffee_ordered(self, brewer, expected):
        result = brewer.was_make_a_coffee_called()
        self.assertEqual(
            expected, result,
            f"Commande de café incorrecte. Attendu: {expected}, Trouvé: {result}"
        )

    def assert_led_warning(self, button_panel, expected):
        self.assertEqual(
            expected, button_panel.get_lungo_warning_state(),
            f"État de la LED incorrect. Attendu: {expected}, Trouvé: {button_panel.get_lungo_warning_state()}"
        )

    def assert_button_pressed(self, button_panel, button_code, pressed=True):
        self.assertEqual(
            pressed, button_panel.is_button_pressed(button_code),
            f"État du bouton {button_code} incorrect. Attendu: {pressed}, Trouvé: {not pressed}"
        )

    def assert_machine_state(self, brewer, no_water=False, is_defaulter=False):
        self.assertEqual(
            no_water, brewer.no_more_water,
            f"Problème de manque d'eau incorrect. Attendu: {no_water}, Trouvé: {brewer.no_more_water}"
        )
        self.assertEqual(
            is_defaulter, brewer.is_defaulter,
            f"Problème de défaillance du hardware incorrect. Attendu: {is_defaulter}, Trouvé: {brewer.is_defaulter}"
        )

    def assert_stirrer_provided(self, cup_provider, expected):
        self.assertEqual(
            expected, cup_provider.was_stirrer_provided(),
            f"Présence de touillette incorrecte. Attendu: {expected}, Trouvé: {cup_provider.was_stirrer_provided()}"
        )

    def assert_pour_sugar(self, brewer, success=False, failure=False):
        pour_sugar_status = brewer.get_pour_sugar_calls()
        self.assertEqual(
            success, all(pour_sugar_status),
            f"Quantité de sucre incorrecte. Attendu: {success}, Trouvé: {pour_sugar_status}"
        )

        self.assertEqual(
            failure, not all(pour_sugar_status),
            f"Quantité de sucre incorrecte. Attendu: {not failure}, Trouvé: {pour_sugar_status}"
        )
    
    def assert_no_sugar(self, brewer):
        self.assertEqual(
            0, len(brewer.get_pour_sugar_calls()),
            f"Quantité de sucre incorrecte. Attendu: 0, Trouvé: {brewer.get_pour_sugar_calls()}"
        )
import unittest
import random
from catan.bank import Bank

class testBank(unittest.TestCase):
    bank = Bank()
    bankSave = Bank()

    """ 
        The bank should be initialised with 19 of each resource, we can return the entire amount of resources
        that are available, or query a specific resource where only the number is returned.
    """

    def testResources(self):
        """ First we are going to confirm the default values for each resource has been correctly applied. """
        self.assertEqual(self.bank.get_bank_resources(), {'forest': 19, 'hills': 19, 'pasture': 19, 'fields': 19, 'mountains': 19})
        self.assertEqual(self.bank.get_bank_resource('forest'), 19)
        self.assertEqual(self.bank.get_bank_resource('hills'), 19)
        self.assertEqual(self.bank.get_bank_resource('pasture'), 19)
        self.assertEqual(self.bank.get_bank_resource('fields'), 19)
        self.assertEqual(self.bank.get_bank_resource('mountains'), 19)

        """ We can now attempt to add a single resource. """
        self.bank.add_bank_resources('forest')
        self.assertEqual(self.bank.get_bank_resource('forest'), 20)

        """ There is another method for adding resources, where we can also specify a number. """
        self.bank.add_bank_resources_with_amount('forest', 10)
        self.assertEqual(self.bank.get_bank_resource('forest'), 30)

        """ We can now attempt to remove a single resource. """
        self.bank.remove_resources('forest')
        self.assertEqual(self.bank.get_bank_resource('forest'), 29)

        """ Adding to the bank resources is also achieved through placement of infrastructure. """
        """ The road placement adds a single resource to forest and hills. """
        self.bank.add_bank_resources_from_placement("road")
        self.assertEqual(self.bank.get_bank_resource('forest'), 30)
        self.assertEqual(self.bank.get_bank_resource('hills'), 20)
        """ The house placement adds a single resource to forest, fields, pasture and hills. """
        self.bank.add_bank_resources_from_placement("house")
        self.assertEqual(self.bank.get_bank_resource('forest'), 31)
        self.assertEqual(self.bank.get_bank_resource('fields'), 20)
        self.assertEqual(self.bank.get_bank_resource('pasture'), 20)
        self.assertEqual(self.bank.get_bank_resource('hills'), 21)
        """ The city placement adds two field resources and 3 mountains. """
        self.bank.add_bank_resources_from_placement("city")
        self.assertEqual(self.bank.get_bank_resource('fields'), 22)
        self.assertEqual(self.bank.get_bank_resource('mountains'), 22)
        """ The dev card placement adds a single resource to pasture, fields and mountains. """
        self.bank.add_bank_resources_from_placement("dev card")
        self.assertEqual(self.bank.get_bank_resource('pasture'), 21)
        self.assertEqual(self.bank.get_bank_resource('fields'), 23)
        self.assertEqual(self.bank.get_bank_resource('mountains'), 23)

    def testDevCards(self):
        """ The initialisation of the Bank class will randomly choose between values stored under
        DEV_CARDS, for consistency we will specify a much smaller list. """
        self.bank.dev_cards = ['road', 'knight', 'victory', 'year', 'monopoly']
        self.assertEqual(self.bank.get_dev_cards(), ['road', 'knight', 'victory', 'year', 'monopoly'])

        """ Using the remove_dev_card() method, the first in the list of dev_cards should be removed
        in this case being the road dev_card. """
        self.bank.remove_dev_card()
        self.assertEqual(self.bank.get_dev_cards(), ['knight', 'victory', 'year', 'monopoly'])

        """ We should be able to shuffle the currently set dev_cards using the shuffled_dev_cards() 
        method, which accepts a list of dev_cards. """
        self.bank.shuffled_dev_cards(self.bank.dev_cards)
        self.assertNotEqual(self.bank.get_dev_cards(), ['knight', 'victory', 'year', 'monopoly'])

    def testBankSave(self):
        """ We can determine what the value when the generate_bank_save() method is called, by
        manually adding the first key/value entry used for dev cards, as we have specified these
        dev cards, we know exactly what to expect, and adding additional key/value entries for each
        of the default resources, which we know each value should be 19. """
        self.bankSave.dev_cards = ['road', 'knight', 'victory', 'year', 'monopoly']
        self.bankSaveResource = {"dev cards": self.bankSave.get_dev_cards()}
        self.bankSaveResource['fields'] = 19
        self.bankSaveResource['forest'] = 19
        self.bankSaveResource['hills'] = 19
        self.bankSaveResource['mountains'] = 19
        self.bankSaveResource['pasture'] = 19

        self.assertEqual(self.bankSave.generate_bank_save(), self.bankSaveResource)

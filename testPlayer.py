import unittest
import sys

sys.path.append("../..")

from catan import Player

class testPlayerClass(unittest.TestCase):
   player = Player("John Smith", blue)
   
   def testPlayer(self):
       self.assertEqual(player.name, "John Smith")


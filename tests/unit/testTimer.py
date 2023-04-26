import unittest
from catan.timer import Timer

""" 
    The timer class stores the time remaining for the game in progress; it has the
    ability to be paused and unpaused, and saves important information to a file. 
"""

class testTimer(unittest.TestCase):
    testScreen = ""

    timer = Timer(testScreen)

    """
        The timer should use a hard coded value of 15 minutes, and should start
        unpaused. The unpaused state should be changeable using the pause() 
        and unpause() methods.
    """

    def testTimerParam(self):
        """ The value is calculated from milliseconds, but using simple multiplication
        we can assert that the value should be 15 minutes. """
        self.assertEqual(self.timer.time, (15*60*1000))

        """ Timer will not be paused by default. """
        self.timer.unpause()
        self.assertEqual(self.timer.paused, False)

        """ Unless the pause method has been called. """
        self.timer.pause()
        self.assertEqual(self.timer.paused, True)

    """ 
        The timer's "save()" method creates a save file called "timer_data.txt". After saving to the
        file, we are going to make changes to the timer's values, then attempt to load the save file and
        see if the values have been correctly stored and can be correctly loaded.
    """

    def testSaveLoad(self):
        """ Set some values then save them to a file. """
        self.timer.time = (15*60*1000)
        self.timer.paused = True
        self.timer.remaining_time = ((15*60*1000)/10)
        self.timer.save()

        """ Change these values but do not save to file. """
        self.timer.time = 100000 
        self.assertEqual(self.timer.time, (100000))
        self.timer.paused = False
        self.assertEqual(self.timer.paused, False)
        self.timer.remaining_time = 10000
        self.assertEqual(self.timer.remaining_time, 10000)

        """ Load the last saved changes from the file, and confirm these values have persisted. """
        self.timer.load()
        self.assertEqual(self.timer.time, (15*60*1000))
        self.assertEqual(self.timer.paused, True)
        self.assertEqual(self.timer.remaining_time, ((15*60*1000)/10))

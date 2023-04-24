import unittest

from catan.timer import Timer

class testTimer(unittest.TestCase):
    testScreen = ""
    
    timer = Timer(testScreen)

    def testTimerParam(self):
        # 900000 calculated from 15 * 60 * 1000 aka. 15 minutes in milliseconds
        self.assertEqual(self.timer.time, (15*60*1000))

        # Timer will not be paused by default
        self.timer.unpause()
        self.assertEqual(self.timer.paused, False)

        # Unless the pause method has been called
        self.timer.pause()
        self.assertEqual(self.timer.paused, True)

    def testSaveLoad(self):
        # Set some values then save them to a file
        self.timer.time = (15*60*1000)
        self.timer.paused = True
        self.timer.remaining_time = ((15*60*1000)/10)
        self.timer.save()

        # Change these values but do not save to file
        self.timer.time = 100000 
        self.assertEqual(self.timer.time, (100000))
        self.timer.paused = False
        self.assertEqual(self.timer.paused, False)
        self.timer.remaining_time = 10000
        self.assertEqual(self.timer.remaining_time, 10000)

        # Load the last saved changes, and confirm the values
        self.timer.load()
        self.assertEqual(self.timer.time, (15*60*1000))
        self.assertEqual(self.timer.paused, True)
        self.assertEqual(self.timer.remaining_time, ((15*60*1000)/10))

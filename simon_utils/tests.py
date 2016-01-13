import unittest
from utils import Timer

class TestTimer(unittest.TestCase):
    def test_timer():
        t = Timer()
        t2 = Timer(3)
        t.update()
        t2.update()

# TODO more tests!

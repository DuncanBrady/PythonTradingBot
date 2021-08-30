import unittest
import sys
sys.path.append("..")

from src.StatBot import StatBot

class TestStatBot(unittest.TestCase):

    def test_construtor(self):
        stat = StatBot(codes=["LUKE", "is", "gay"])

    
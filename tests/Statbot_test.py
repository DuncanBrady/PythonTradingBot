import unittest
import sys
sys.path.append("..")

from src.StatBot import StatBot

class TestStatBot(unittest.TestCase):

	def test_construtor(self):
		stckcodes = ["TST", "ISA", "EXR"]
		stat = StatBot(codes=stckcodes)
		for code in stckcodes:
			self.assertEqual(stat.get_mv_avg(code), 0.0)
			self.assertEqual(stat.get_rsi(code), 0.0)
			self.assertEqual(stat.get_price(code), {"open": [], "high":[], "close": []})


if __name__ == '__main__':
	unittest.main()  
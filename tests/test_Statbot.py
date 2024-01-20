import unittest
import sys
import random
import numpy as np
from src.StatBot import StatBot
sys.path.append("..")


class TestStatBot(unittest.TestCase):

    def test_construtor(self):
        stockcodes = ["TST", "ISA", "EXR"]
        stat = StatBot(codes=stockcodes)
        for code in stockcodes:
		    self.assertEqual(stat.get_mv_avg(code), 0.0)
		    self.assertEqual(stat.get_rsi(code), 0.0)
			self.assertEqual(stat.get_price(code), {"open": [], "high":[], "close": [], "low": []})

    def test_get_rsi(self):
        stockcodes = ["APPL", "TSLA", "EXR"]
        stat = StatBot(codes=stockcodes)
    stat.set_rsi("EXR", 34.00)
    self.assertEqual(stat.get_rsi("EXR"), 34.00)


    def test_get_price(self):
    data = {
        "EXR": {
            "open": 1.00,
            "high": 2.00,
            "close": 1.5,
            "volume": 2000000,
            "low": 0
        },

        "TRT": {
            "open": 1.14,
            "high": 1.20,
            "close": 90,
            "volume": 1000,
            "low": 0
        },

        "APPL": {
            "open": 145.00,
            "high": 150.00,
            "close": 145.00,
            "volume": 4350060,
            "low": 0
        }
    }

    stockcodes = ["APPL", "TRT", "EXR"]
    stat = StatBot(codes=stockcodes)
    stat.process_incoming(data)
    self.assertEqual(stat.get_price("EXR"), {"open": [1.0], "high": [2.0], "close": [1.5], "low": [0]})


    def test_mv_avg(self):
        data = {
            "EXR": {
                "open": 1.00,
                "high": 2.00,
                "close": 1.5,
                "volume": 2000000,
                "low": 0
            }
            }

        data2 = {
            "EXR": {
                "open": 1.00,
                "high": 2.00,
                "close": 2.0,
                "volume": 2000000,
                "low": 0
            }
        }

        data3 = {
            "EXR": {
                "open": 1.00,
                "high": 2.00,
                "close": 3.00,
                "volume": 2000000,
                "low": 0
            }
        }

        stockcodes = ["APPL", "TRT", "EXR"]
        stat = StatBot(codes=stockcodes)

        stat.process_incoming(data)
        self.assertEqual(stat.get_mv_avg("EXR"), 1.5)

        stat.process_incoming(data2)
        self.assertEqual(stat.get_mv_avg("EXR"), 1.75)

        stat.process_incoming(data3)
        self.assertEqual(stat.get_mv_avg("EXR"), 6.5 / 3)

    def test_heaps_prices(self):
        stockcodes = ["APPL", "TRT", "EXR"]
        stat = StatBot(codes=stockcodes)

        data = {
            "EXR": {
                "open": 1.00,
                "high": 2.00,
                "close": 1.5,
                "volume": 2000000,
                "low": 0
                }
            }


        prices = []
        for i in range(6):
            prices.append(random.randint(0,10))
            prices1 = prices[0:5]
            prices2 = prices[1:6]

        for num in prices1:
            data["EXR"]['close'] = num
            stat.process_incoming(data)

        self.assertEqual(stat.get_mv_avg("EXR"), sum(prices1) / len(prices1))

        for num in prices2:
        data["EXR"]['close'] = num
        stat.process_incoming(data)

        self.assertEqual(stat.get_mv_avg("EXR"), sum(prices2) / len(prices2))

    def test_calc_bands(self):
        stockcodes = ["EXR"]
        stat = StatBot(codes = stockcodes)

        data = {
            "EXR": {
                "open": 1.00,
                "high": 2.00,
                "close": 1.5,
                "volume": 2000000,
                "low": 0
            }
        }

        prices = []
        for i in range(6):
            prices.append(random.randint(0,10))

        prices1 = prices[0:5]
        prices2 = prices[1:6]

        for num in prices1:
            data["EXR"]['close'] = num
            stat.process_incoming(data)

        lower = sum(prices1)/len(prices1) - 2*np.std(prices1)
        upper = sum(prices1)/len(prices1) + 2*np.std(prices1)

        self.assertEqual(stat.calc_bands("EXR"), (lower, upper))


    def test_calc_rsi(self):
		bot = StatBot(codes=["EXR"],rsi={}, past_prices={})
		prices = [1.5, 2.0, 1.75, 1.3, 1.8]
		for price in prices:
			bot.past_prices["EXR"]["close"].insert(0,price)
			bot.rsi_calc("EXR")
			self.assertEqual(round(bot.get_rsi("EXR"), 2), 41.18)
			prices = [6001,7550,4431,9435,8453]
			bot.past_prices["EXR"]["close"] = []
		for price in prices:
			bot.past_prices["EXR"]["close"].insert(0,price)
			bot.rsi_calc("EXR")
			self.assertEqual(round(bot.get_rsi("EXR"), 2), 38.49)

if __name__ == '__main__':
    unittest.main()

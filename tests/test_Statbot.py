import unittest
import random
import numpy as np
from src.StatBot import StatBot


class TestStatBot(unittest.TestCase):

    def test_constructor(self):
        stocktickers = ["TST", "ISA", "EXR"]
        stat = StatBot(tickers=stocktickers)
        for ticker in stocktickers:
            self.assertEqual(stat.get_mv_avg(ticker), 0.0)
            self.assertEqual(stat.get_rsi(ticker), 0.0)
            self.assertEqual(
                stat.get_price(ticker),
                {"open": [], "high": [], "close": [], "low": []}
            )

    def test_get_rsi(self):
        stocktickers = ["APPL", "TSLA", "EXR"]
        stat = StatBot(tickers=stocktickers)
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

        stocktickers = ["APPL", "TRT", "EXR"]
        stat = StatBot(tickers=stocktickers)
        stat.process_incoming(data)
        self.assertEqual(
            stat.get_price("EXR"),
            {"open": [1.0], "high": [2.0], "close": [1.5], "low": [0]}
        )

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

        stocktickers = ["APPL", "TRT", "EXR"]
        stat = StatBot(tickers=stocktickers)

        stat.process_incoming(data)
        self.assertEqual(stat.get_mv_avg("EXR"), 1.5)

        stat.process_incoming(data2)
        self.assertEqual(stat.get_mv_avg("EXR"), 1.75)

        stat.process_incoming(data3)
        self.assertEqual(stat.get_mv_avg("EXR"), 6.5 / 3)

    def test_heaps_prices(self):
        stocktickers = ["APPL", "TRT", "EXR"]
        stat = StatBot(tickers=stocktickers)

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
            prices.append(random.randint(0, 10))
            prices1 = prices[0:5]
            prices2 = prices[1:6]

        for num in prices1:
            data["EXR"]['close'] = num
            stat.process_incoming(data)

        self.assertEqual(stat.get_mv_avg("EXR"), sum(prices1) / len(prices1))

        for num in prices2:
            data["EXR"]['close'] = num
            stat.process_incoming(data)

        self.assertEqual(
            stat.get_mv_avg("EXR"),
            (sum(prices2 + prices1)) / (len(prices2) + len(prices1))
        )

    def test_calc_bands(self):
        stocktickers = ["EXR"]
        stat = StatBot(tickers=stocktickers)

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
            prices.append(random.randint(0, 10))

        prices1 = prices[0:5]
        # prices2 = prices[1:6]

        for num in prices1:
            data["EXR"]['close'] = num
            stat.process_incoming(data)

        lower = sum(prices1) / len(prices1) - 2 * np.std(prices1)
        upper = sum(prices1) / len(prices1) + 2 * np.std(prices1)

        lower_rounded = round(lower, 2)
        upper_rounded = round(upper, 2)

        bands = stat.calc_bands("EXR")
        bands_rounded = tuple(round(element, 2) for element in bands)

        self.assertEqual(bands_rounded, (lower_rounded, upper_rounded))

    def test_calc_rsi(self):
        bot = StatBot(tickers=["EXR"], rsi={}, past_prices={})

        prices = [1.5, 2.0, 1.75, 1.3, 1.8]
        for price in prices:
            bot.past_prices["EXR"]["close"].insert(0, price)
            bot.rsi_calc("EXR")

        self.assertEqual(round(bot.get_rsi("EXR"), 2), 41.18)

        bot.past_prices["EXR"]["close"] = []
        prices = [6001, 7550, 4431, 9435, 8453]
        for price in prices:
            bot.past_prices["EXR"]["close"].insert(0, price)
            bot.rsi_calc("EXR")

        self.assertEqual(round(bot.get_rsi("EXR"), 2), 38.49)


if __name__ == '__main__':
    unittest.main()

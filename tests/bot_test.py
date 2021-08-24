import unittest
import sys
sys.path.append("..")


from src.Bot import Bot

class TestBot(unittest.TestCase):
    
    def test_buy(self):
        bot = Bot(balance = 1000, position = [])
        bot.buy("EXR", 1.00, 500)
        self.assertEqual(bot.get_balance(), 500)
        self.assertEqual(bot.get_position(), [{
            "code" : "EXR",
            "value" : 1.00,
            "num_shares" : 500,
            "total_invested" : 500
        }])

    def test_sell(self):
        bot = Bot(balance = 1000, position = [])
        bot.buy("EXR", 1.00, 500)
        bot.sell("EXR", 2.00)
        self.assertEqual(bot.balance, 1500)



if __name__ == "__main__":
    unittest.main()
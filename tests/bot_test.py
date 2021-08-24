import unittest
import sys
sys.path.append("..")


from src.Bot import Bot

class TestBot(unittest.TestCase):
    
    def setUp(self):
        self.bot = Bot(balance=1000)
    
    def test_buy(self):
        self.bot.buy("EXR", 1.00, 500)
        self.assertEquals(self.bot.get_balance(), 500)
        self.assertEquals(self.bot.get_position(), [{
            "code" : "EXR",
            "value" : 1.00,
            "num_shares" : 500
        }])




if __name__ == "__main__":
    unittest.main()
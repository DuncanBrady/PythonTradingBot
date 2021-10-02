import unittest
import sys
sys.path.append("..")


from src.Bot import *

class TestBot(unittest.TestCase):
    
    def test_add_buy(self):
        bot = Bot(balance = 1000, position = [])
        bot.add_buy("EXR", 1.00, 500)
        self.assertEqual(bot.get_balance(), 500)
        self.assertEqual(bot.get_position(), [{
            "code" : "EXR",
            "current_price" : 1.00,
            "value" : 1.00,
            "num_shares" : 500,
            "total_invested" : 500
        }])

    def test_add_sell(self):
        bot = Bot(balance = 1000, position = [])
        bot.add_buy("EXR", 1.00, 500)
        bot.add_sell("EXR", 2.00)
        self.assertEqual(bot.get_balance(), 1500)

    def test_stop_loss(self):
        bot = Bot(balance = 1000, position = [])
        bot.add_buy("TRT", 3.00, 800)
        self.assertEqual(bot.get_balance(), 200)
        
        bot.get_position()[0]['current_price'] = 2.00
        bot.check_sell()
        
        self.assertEqual(bot.get_position(), [])
        self.assertEqual(bot.get_balance(),  733.3333333333334)
        
    
    def test_add_buy_exception(self):
        bot = Bot(balance = 1000, position = [])
        with self.assertRaises(Exception):
            bot.add_buy("TRT", 3.00, 2000)
    
    
    
    def test_add_sell_exception(self):
        bot = Bot(balance = 1000, position = [])
        with self.assertRaises(Exception):
            bot.add_sell("EXR", 2.00)
    
    
    
    def test_process_data(self):
        bot = Bot(balance = 1000, position = [])
        bot.add_buy("APPL", 130.00, 1000)
        
        bot.call_api()
        
        self.assertEqual(bot.get_position()[0], {
            "code" : "APPL",
            "current_price" : 130.00,
            "value" : 130.00,
            "num_shares" : 1000/130,
            "total_invested" : 1000
        })
    
    def test_get_score(self):
        bot = Bot(balance = 1000, position = [])
        result = bot.get_score(BUY, 50, 0.1)
        self.assertEqual(result, 0.1/50)
        
        
        
        

if __name__ == "__main__":
    unittest.main()
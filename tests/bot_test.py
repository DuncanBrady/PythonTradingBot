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
            "current_price" : 1.00,
            "value" : 1.00,
            "num_shares" : 500,
            "total_invested" : 500
        }])

    def test_sell(self):
        bot = Bot(balance = 1000, position = [])
        bot.buy("EXR", 1.00, 500)
        bot.sell("EXR", 2.00)
        self.assertEqual(bot.get_balance(), 1500)

    def test_stop_loss(self):
        bot = Bot(balance = 1000, position = [])
        bot.buy("TRT", 3.00, 800)
        self.assertEqual(bot.get_balance(), 200)
        
        bot.get_position()[0]['current_price'] = 2.00
        bot.check_stop_loss()
        
        self.assertEqual(bot.get_position(), [])
        self.assertEqual(bot.get_balance(),  733.3333333333334)
        
    
    def test_buy_exception(self):
        bot = Bot(balance = 1000, position = [])
        with self.assertRaises(Exception):
            bot.buy("TRT", 3.00, 2000)
    
    
    
    def test_sell_exception(self):
        bot = Bot(balance = 1000, position = [])
        with self.assertRaises(Exception):
            bot.sell("EXR", 2.00)
    
    
    
    def test_process_data(self):
        bot = Bot(balance = 1000, position = [])
        bot.buy("APPL", 130.00, 1000)
        
        bot.periodic_call_api("url")
        
        self.assertEqual(bot.get_position()[0], {
            "code" : "APPL",
            "current_price" : 145.00,
            "value" : 130.00,
            "num_shares" : 1000/130,
            "total_invested" : 1000
        })
        

if __name__ == "__main__":
    unittest.main()
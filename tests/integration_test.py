from random import random
import unittest
import sys
import random
import numpy as np
sys.path.append("..")

from src.StatBot import *
from src.Bot import *

class TestIntegration(unittest.TestCase):
    
    def test_check_buy(self):
        bot = Bot(balance = 1000, position = [])
        stockcodes = ["TST", "ISA", "EXR"]
        stat = StatBot(codes=stockcodes)

        
        # bot.buying = [
        #     {
        #         "code" : "TST",
        #         "current_price" : 10,
        #         "value" : 15,
        #         "num_shares" : 5,
        #         "total_invested" : 1000,
        #     },
            
        #     {
        #         "code" : "EXR",
        #         "current_price" : 10,
        #         "value" : 15,
        #         "num_shares" : 5,
        #         "total_invested" : 1000,
        #     },
            
        #     {
        #         "code" : "ISA",
        #         "current_price" : 10,
        #         "value" : 15,
        #         "num_shares" : 5,
        #         "total_invested" : 1000,
        #     }
        # ]
        
        bot.position = [
            {
                "code" : "TST",
                "current_price" : 10,
                "value" : 15,
                "num_shares" : 5,
                "total_invested" : 1000,
            },
            
            {
                "code" : "EXR",
                "current_price" : 10,
                "value" : 15,
                "num_shares" : 5,
                "total_invested" : 1000,
            },
            
            {
                "code" : "ISA",
                "current_price" : 10,
                "value" : 15,
                "num_shares" : 5,
                "total_invested" : 1000,
            }
        ]
        
        data = {}
        for code in stockcodes:
            data[code] = {
                "open" : random.random() * 3,
                "high" : random.random() * 3,
                "low" : random.random() * 3,
                "close" : random.random() * 3,
            }
             
        stat.set_rsi("TST", 1)
        stat.set_rsi("ISA", 5)
        stat.set_rsi("EXR", 100)
        
        bot.check_buy(data)
        print(len(bot.buying))
        
        self.assertEqual(bot.buying, [
            
            
            {
                "code" : "TST",
                "current_price" : 10,
                "value" : 15,
                "num_shares" : 5,
                "total_invested" : 1000,
            },
            {
                "code" : "ISA",
                "current_price" : 10,
                "value" : 15,
                "num_shares" : 5,
                "total_invested" : 1000,
            },
            
            {
                "code" : "EXR",
                "current_price" : 10,
                "value" : 15,
                "num_shares" : 5,
                "total_invested" : 1000,
            }
        ])
        
        
        



if __name__ == '__main__':
    unittest.main()
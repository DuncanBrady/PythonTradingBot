
'''
 Statistical Analysis tools for python trading bot, includes
    - Bolinger Bands
    - RSI Calculations
Written: August 2021
Author: Robert Brady & Luke Banicevic 
'''

class StatBot:

    def __init__(self, mv_avg = {}, RSI = {}, past_prices = {}, codes = []):
        self.mv_avg = mv_avg
        self.past_prices = past_prices
        self.RSI = RSI
        self.codes
        if codes is not None:
            for key in codes:
                self.mv_avg[str(key)] = 0.0
                self.past_prices[str(key)] = []
                self.RSI[str(key)] = 0.0

    def          

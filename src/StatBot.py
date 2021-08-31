
'''
 Statistical Analysis tools for python trading bot, includes
    - Bolinger Bands
    - RSI Calculations
Written: August 2021
Author: Robert Brady & Luke Banicevic 
'''

import numpy as np
import scipy as sp


class StatBot:

    def __init__(self, mv_avg = {}, RSI = {}, past_prices = {}, codes = []):
        """Constructor for the StatBot class

        Args:
            mv_avg (dict, optional): Stores the moving averages for all stock codes. Defaults to {}.
            RSI (dict, optional): Stores the RSI's for all stock codes . Defaults to {}.
            past_prices (dict, optional): Stores the past prices of the monitored stock codes. Defaults to {}.
            codes (list, optional): Stock codes which are set to be monitored. Defaults to [].
        """
        self.mv_avg = mv_avg
        self.past_prices = past_prices
        self.RSI = RSI
        if codes is not None:
            self.build_dicts(codes)

    def calc_bands(self, mv_avg):
        pass
    
    def rsi_calc(self):
        pass

    def update_code(self, code, incoming_data):
        pass

    def process_incoming(self, incoming_data):
        for key in incoming_data:
            update_code(str(key), incoming_data[key])
        return incoming_data

    def set_mv_avg(self, code, mv_avg):
        self.mv_avg[code] = mv_avg

    def set_rsi(self, code, rsi):
        if self.rsi.get(code):
            self.rsi[code] = rsi 
   
    def get_mv_avg(self, code):
        return self.mv_avg.get(code, None)

    def build_dicts(self, codes): 
        """Builds the statsbots collection of data as stock codes as keys

        Args:
            codes (list[string]): List of Stock codes which are being monitored
        """
        for key in codes:
            self.mv_avg[str(key)] = 0.0
            self.past_prices[str(key)] = {"open" :[], "high": [], "close": []}
            self.rsi[str(key)] = 0.0   
    
    def calc_bands(self, code):
        """Calculates upper and lower bolinger band values for a given stock
        bolinger bands represent a set number of standard deviations above or below the moving average
        close

        Args:
            code (string): code for the given stock in question
        """
        
        
        #retrieve the past prices of the stock

        #calculate the standard deviation

        #retrive the moving average

        #return tuple of upper and lower values

    def rsi_calc(self):
        pass

    def update_code(self, code, incoming_data):
        pass

    def process_incoming(self, incoming_data):
        for key in incoming_data:
            update_code(str(key), incoming_data[key])
        return incoming_data

    def set_mv_avg(self, code, mv_avg):
        self.mv_avg[code] = mv_avg

    def set_rsi(self, code, rsi):
        if self.rsi.get(code):
            self.rsi[code] = rsi 
   
    def get_mv_avg(self, code):
        return self.mv_avg.get(code, None)
    
    def get_price(self, code):
        return self.past_prices.get(code, None)

    def get_rsi(self, code):
        return self.rsi.get(code, None)
    def calc_bands(self, mv_avg):
        pass
    
    def rsi_calc(self):
        pass

    def update_code(self, code, incoming_data):
        pass


    
    

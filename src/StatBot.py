
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
        self.codes
        if codes is not None:
            self.build_dicts(codes)

    def build_dicts(self, codes): 
        """Builds the statsbots collection of data as stock codes as keys

        Args:
            codes ([type]): [description]
        """
        for key in codes:
            self.mv_avg[str(key)] = 0.0
            self.past_prices[str(key)] = []
            self.RSI[str(key)] = 0.0   

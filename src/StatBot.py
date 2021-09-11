'''
 Statistical Analysis tools for python trading bot, includes
    - Bolinger Bands
    - rsi Calculations
Written: August 2021
Author: Robert Brady & Luke Banicevic 
'''

import numpy as np
import scipy as sp


class StatBot:

    def __init__(self, mv_avg = {}, rsi = {}, past_prices = {}, codes = []):
        """Constructor for the StatBot class
        Args:
            mv_avg (dict, optional): Stores the moving averages for all stock codes. Defaults to {}.
            rsi (dict, optional): Stores the rsi's for all stock codes . Defaults to {}.
            past_prices (dict, optional): Stores the past prices of the monitored stock codes. Defaults to {}.
            codes (list, optional): Stock codes which are set to be monitored. Defaults to [].
        """
        self.mv_avg = mv_avg
        self.past_prices = past_prices
        self.rsi = rsi
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
            self.rsi[str(key)] = {
                "rsi" : 0.0,
                "up_moves" : [],
                "down_moves" : []
            }   
    
    def calc_bands(self, code):
        """Calculates upper and lower bolinger band values for a given stock
        bolinger bands represent a set number of standard deviations above or below the moving average
        close
        Args:
            code (string): code for the given stock in question
        """
        
        #retrieve the past prices of the stock
        past_prices = self.get_price(code)
            
        #calculate the standard deviation
        std = np.std(past_prices['close'])

        #retrieve the moving average
        mv_avg = self.get_mv_avg(code)
        
        # return tuple of upper and lower values
        return (mv_avg - 2*std, mv_avg + 2*std)

    def rsi_calc(self, code):
        """Calculates the rsi of a particular stock code given its average up and down moves over a certain period

        Args:
            code (string): stock code of the given stock
        """
        self.rsi_update_moves(code)
        
        # rsi calculation

        avg_up = abs(sum(self.rsi[code]['up_moves']) / len(self.rsi[code]['up_moves']))
        avg_down = abs(sum(self.rsi[code]['down_moves']) / len(self.rsi[code]['down_moves']))
        if avg_up == 0:
           avg_up = 1
        rs = avg_down/avg_up
        rsi = 100 - 100/(1+rs)
        self.set_rsi(code, rsi)
        
    def rsi_update_moves(self, code):
        """Updates the list of up and down moves for a stock in a given period

        Args:
            code (string): stock code being updated
        """
        try:
            diff = self.get_price(code)['close'][0] - self.get_price(code)['close'][1]
        except:
            diff = 0
        if diff > 0:
            self.rsi[code]['up_moves'].insert(0, diff)
        elif diff < 0:
            self.rsi[code]['down_moves'].insert(0, diff)
        else:
            self.rsi[code]['up_moves'].insert(0, 0)
            self.rsi[code]['down_moves'].insert(0, 0)
        
        self.rsi[code]['up_moves'] = self.rsi[code]['up_moves'][:5]
        self.rsi[code]['down_moves'] = self.rsi[code]['down_moves'][:5]
        
    
    def update_prices(self, code, new_prices):
        """Helper function which updates the old_prices given new ones

        Args:
            old_prices (dict): old prices of a given stock code
            new_prices (dict): new prices of a given stock code
        """
        
        
        old_prices = self.get_price(code)
        
        if old_prices is not None:
            old_prices['open'].insert(0, new_prices['open'])
            old_prices['close'].insert(0,new_prices['close'])
            old_prices['high'].insert(0,new_prices['high'])
            
            old_prices['open'] = old_prices['open'][:5]
            old_prices['close'] = old_prices['close'][:5]
            old_prices['high'] = old_prices['high'][:5]
        
    def update_mv_avg(self, code):
        """Updates the mv avg for a stock code

        Args:
            code (string): Stock code for the given stock
        """
        
        
        # new mvg average is equal to sum of the close prices divided by the number of prices stored
        new_mv_avg = sum(self.get_price(code)['close']) / len(self.get_price(code)['close'])
        self.set_mv_avg(code, new_mv_avg)

    def process_incoming(self, incoming_data):
        """Process incoming of stock codes and their corresponding price actions

        Args:
            incoming_data (dict): data of stock codes and price information
        """
        for key in incoming_data:
            self.update_prices(key, incoming_data.get(key))
            self.update_mv_avg(key)
         #   self.rsi_calc(key)


    '''
        Getters and Setters
    '''
    def set_mv_avg(self, code, mv_avg):
        self.mv_avg[code] = mv_avg

    def set_rsi(self, code, rsi):
        if self.rsi.get(code, None) is not None:
            self.rsi.get(code)['rsi'] = rsi 
   
    def get_mv_avg(self, code):
        return self.mv_avg.get(code, None)
    
    def get_price(self, code):
        return self.past_prices.get(code, None)

    def get_rsi(self, code):
        return self.rsi.get(code, None).get('rsi')

    

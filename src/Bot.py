'''
constants:
    - stop loss percentage : eg 20%
    - balance : double 
    - 


position = [
    {
        "code" : 'XRP',
        "value" : 2.00,
        "number_of_shares" : 5000.0
    }
]

def check_stoploss(self):
 ---> compare value to current_price
    ---> if difference > stop_loss_percent
        ---> sell


'''

import json
import requests
import time
import datetime
import calendar
import sys
 
sys.path.append("..")

from src.StatBot import StatBot

class Bot:
    def __init__(self, balance=0.0, stop_loss=.125, profit_take = 1.25, position=[], position_limit = 10):
        self.balance = balance
        self.stop_loss = stop_loss
        self.profit_take = profit_take
        self.position = position
        self.POSITION_LIMIT = position_limit
        self.statbot = StatBot(codes=[])
    
        
    '''
        Getters and Setters
    '''
    def set_stop_loss(self, stop_loss):
        self.stop_loss = stop_loss

    def set_balance(self, balance):
        self.balance = balance
        
    def set_position(self, position):
        self.position = position
    
    def get_balance(self):
        return self.balance

    def get_stop_loss(self):
        return self.stop_loss

    def get_position(self):
        return self.position
    
    '''
        Static methods
    '''
    @staticmethod
    def format_data(data):
        """Formats the data in a format the bot can understand

        Args:
            data (json/dict): data that is to be formatted

        Returns:
            list[dict]: list of dicts the bot can use to update its state
        """
        list_data = []
        for key in data:
            stock_object = {
                "code" : key,
                "price" : data[key]['close']
            }
            
            list_data.append(stock_object)

        return list_data
    
    @staticmethod
    def create_position_object(code, price, money_invested):
        """Creates a new position object for a given stock bought

        Args:
            code (string): Code of the given stock
            price (double ): price of the given stock
            money_invested (double): money which is invested to buy the given stock

        Returns:
            dict: position object
        """
        return {
            "code" : code,
            "current_price" : price,
            "value" : price,
            "num_shares" : money_invested / price,
            "total_invested" : money_invested
        }
    @staticmethod
    def update_position_object(share_object, price, money_invested):
        """Updates a given position object in the bots position

        Args:
            share_object (dict): given share object
            price (double): price of the given stock/share
            money_invested (double): money which is invested
        """
        share_object['total_invested'] += money_invested
        share_object['num_shares'] += money_invested / price
        share_object['value'] = share_object['total_invested'] / share_object['num_shares']
    
    def build_data(self):
        """Builds the data used by the bot into the correct format

        Returns:
            dict: Dictionary containing codes as keys and price information objects as values
        """
        data = {}
        for code in self.statbot.get_codes():
            data[code] = self.call_api(baseId=code)

        return data


    def buy(self, code, price, money_invested):
        """Buys a particular stock code at a given price, which a portion of money invested

        Args:
            code (string): Code of the given stock
            price (double): price of the given stock
            money_invested (double): money which is being invested

        Raises:
            Exception: When the bot doesnt have enough money to make the purchase
        """
        if self.balance - money_invested < 0:
            raise Exception("Not enough money to buy")
        if len(self.get_position()) >= self.POSITION_LIMIT:
            raise Exception("To many stocks in position")

        self.set_balance(self.get_balance() - money_invested)
        
        # if the code is already in the list, try and find it
        share_object = [x for x in self.get_position() if x['code'] == code]
        
        if len(share_object) == 0:
            self.position.append(self.create_position_object(code,price,money_invested))  
        else:
            self.update_position_object(share_object[0], price, money_invested)
    
    
    def update_current_prices(self, data):
        """Updates the current prices of stocks in the bots position

        Args:
            data (list[dict]): Assuming this is a list of dictionaries
        """
        for stock in data:
            code = stock['code']
            current_price = stock['price']
            for my_position in self.position:
                if my_position['code'] == code:
                    my_position['current_price'] = current_price
        
    def get_ttlval_pos(self):
        """Gets the total value of the bots position

        Returns:
            double: total value of the bots position
        """
        total = 0
        for my_position in self.position:
            total += my_position['current_price'] * my_position['num_shares']

        return total

    
    def check_sell(self, data={}):
        """Checks the bots position for a potential sell opportunity
        """
        
        to_sell = []
        
        for my_position in self.position:
            
            # compare current_price with value
            actual_value = my_position['current_price'] * my_position['num_shares']
            bought_value =  my_position['total_invested']
            
            if bought_value * (1 - self.stop_loss) >= actual_value or bought_value * self.profit_take <= actual_value:
                to_sell.append(my_position)
            elif data[my_position["code"]]["high"] >= self.statbot.calc_bands()[1] and self.statbot.get_rsi(my_position["code"]) >= 70:
                to_sell.append(my_position)
        
        for my_position in to_sell:
            self.sell(my_position['code'], my_position['current_price'])
    
    def sell(self, code, sell_price):
        """Sells a particular stock at a given sell price

        Args:
            code (string): Code of the given stock
            sell_price (double): Sell price of the given stock
        """
        sell_object = [x for x in self.get_position() if x['code'] == code][0]
        if sell_object is None:
            raise Exception("Stock not in position")
        self.set_balance(self.get_balance() + sell_price * sell_object['num_shares'])
        self.position.remove(sell_object)


    def call_api(self, crypto = "ADA"):
        """Makes a periodic request to some api to get stock information

        Args:
            url (string): url of the given api
        """
        now = datetime.datetime.utcnow()
        before = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
        
        start =  calendar.timegm(before.timetuple()) * 1000
        end = calendar.timegm(now.timetuple()) * 1000
        
        CANDLE_DATA = f'https://api.kraken.com/0/public/OHLC'
        pair = f'{crypto}AUD'
        PARAMS = {
            'pair' : pair,
            'interval' : '1',
            'since' : end
        }
        
        
        response = requests.get(url = CANDLE_DATA, params = PARAMS)
        
        while response.status_code != 200:
            time.sleep(2)
            response = requests.get(url = CANDLE_DATA, params = PARAMS)
        
        data = response.json()
    

        return data        
                
        
    def process_data(self):
        """Processes price information gathered from api call and executes functions based on data
        """
        data = self.build_data()
        self.statbot.process_incoming(data)
        self.update_current_prices(self.format_data(data))
        self.check_sell()
        self.check_buy(data)
        
        
    
    def check_buy(self, data):
        """Check if there is a favourable buy situation for the bots list of stocks

        Args:
            data (dict/json): Json object containing stock information at a particular time
        """
        for my_position in self.position:
            high_price = data[my_position['code']]['high']
            value_that_we_have = my_position['value']
            
            # if one of our stocks has dropped by 5%, buy more of it in the hopes that it will go up
            if value_that_we_have * .95 >= high_price:
                self.buy(my_position['code'], high_price, my_position['total_invested'] * 0.025)
        
        # check for new stock
        for key in data:
            #if key doesnt exist in position 
            if not any(key in pos for pos in self.position):
                if data[key]["close"] < self.statbot.calc_bands()[0] and self.statbot.get_rsi(key) < 30:
                    #access exchange api to purchase more stock
                    self.buy(key, data[key]["close"], 500)

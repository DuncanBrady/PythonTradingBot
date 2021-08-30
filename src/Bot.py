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

class Bot:
    def __init__(self, balance=0.0, stop_loss=.125, position=[], position_limit = 10):
        self.balance = balance
        self.stop_loss = stop_loss
        self.position = position
        self.POSITION_LIMIT = position_limit
    
        
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

    
    def check_stop_loss(self):
        """Checks the bots position for stop loss
        """
        
        to_sell = []
        
        for my_position in self.position:
            
            # compare current_price with value
            actual_value = my_position['current_price'] * my_position['num_shares']
            bought_value =  my_position['total_invested']
            
            if bought_value * (1 - self.stop_loss) >= actual_value:
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


    def periodic_call_api(self, url):
        """Makes a periodic request to some api to get stock information

        Args:
            url (string): url of the given api
        """
        
        # Example data sent back by api call
        data = {
            "EXR" : {
                "open" : 1.00,
                "high" : 2.00,
                "close" : 1.5,
                "volume" : 2000000
            },
            
            "TRT" : {
                "open" : 1.14,
                "high" : 1.20,
                "close" : 90,
                "volume" : 1000
            },
            
            "APPL" : {
                "open" : 145.00,
                "high" : 150.00,
                "close" : 145.00,
                "volume" : 4350060
            }
        }
        
        
        # process the data sent back by the api, which will be some json object
        self.process_data(data)
    
    
    def process_data(self, data):
        """Processes the json passed in

        Args:
            data (dict): dictionary/json object
        """
        self.update_current_prices(self.format_data(data))
        self.check_stop_loss()
        self.check_buy(data)
        
    
    def check_buy(self, data):
        """Check if there is a favourable buy situation for the bots list of stocks

        Args:
            data (dict/json): Json object containing stock information at a particular
        """
        for my_position in position:
            high_price = data[my_position['code']]['high']
            value_that_we_have = my_position['value']
            
            # if one of our stocks has dropped by 5%, buy more of it in the hopes that it will go up
            if value_that_we_have * .95 >= high_price:
                self.buy(my_position['code'], high_price, my_position['total_invested'] * 0.025)
        
        
        
        # checking for new stocks
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
    def __init__(self, balance=0.0, stop_loss=.2, position=[]):
        self.balance = balance
        self.stop_loss = stop_loss
        self.position = position
    
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
        for my_position in self.position:
            
            # compare current_price with value
            actual_value = my_position['current_price'] * my_position['num_shares']
            bought_value =  my_position['total_invested']
            
            if bought_value * (1 - self.stop_loss) >= actual_value:
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
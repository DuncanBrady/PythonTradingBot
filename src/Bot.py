'''
    Description: Trading Bot which uses the Bollinger Band trading strategy
    exchange.
    Author: Luke Banicevic & Robert Brady
    Date: 18/09/2021
'''

from src.StatBot import StatBot

TIME = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
BUY = 1
SELL = 0


class Bot():
    def __init__(self,
                 balance=0.0,
                 stop_loss=.125,
                 profit_take=1.25,
                 position=[],
                 position_limit=10,
                 codes=[]):

        self.codes = codes
        self.balance = balance
        self.stop_loss = stop_loss
        self.profit_take = profit_take
        self.position = position
        self.POSITION_LIMIT = position_limit
        self.stat_bot = StatBot(codes=codes)
        self.buying = []
        self.selling = []

    '''
        Getters and Setters
    '''

    def set_balance(self, balance):
        self.balance = balance

    def get_balance(self):
        return self.balance

    def get_position(self):
        return self.position

    def get_codes(self):
        return self.codes

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
                "code": key,
                "price": data[key]['close']
            }

            list_data.append(stock_object)

        return list_data

    @staticmethod
    def create_position_object(code, price, money_invested):
        """Creates a new position object for a given stock bought

        Args:
            code (string): Code of the given stock
            price (double ): price of the given stock
            money_invested (double): money invested to buy the given stock

        Returns:
            dict: position object
        """
        return {
            "code": code,
            "current_price": price,
            "value": price,
            "num_shares": money_invested / price,
            "total_invested": money_invested
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
        share_object['value'] = \
            share_object['total_invested'] / share_object['num_shares']

    def build_data(self):
        """Builds the data used by the bot into the correct format

        Returns:
            dict: Dictionary containing codes and price objects
        """
        data = {}
        for code in self.get_codes():
            value = self.call_api(crypto=code)
            data[code] = {

                'open': float(value[OPEN]),
                'high': float(value[HIGH]),
                'low': float(value[LOW]),
                'close': float(value[CLOSE])
            }

        return data

    def buy(self, code, price, money_invested):
        """Buys a particular stock code at a given price

        Args:
            code (string): Code of the given stock
            price (double): price of the given stock
            money_invested (double): money which is being invested

        Raises:
            Exception: Bot doesnt have enough money to make the purchase
        """
        if self.balance - money_invested < 0:
            raise Exception("Not enough money to buy")
        if len(self.get_position()) >= self.POSITION_LIMIT:
            raise Exception("To many stocks in position")

        self.set_balance(self.get_balance() - money_invested)

        # if the code is already in the list, try and find it
        share_object = [x for x in self.get_position() if x['code'] == code]

        if len(share_object) == 0:
            new_position_object = self.create_position_object(
                code,
                price,
                money_invested
            )
            self.position.append(
                self.create_position_object(code, price, money_invested)
            )
            self.buying.append(new_position_object)
        else:
            self.update_position_object(share_object[0], price, money_invested)
            self.buying.append(share_object[0])

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
        rank_dict = {}
        for my_position in self.position:

            # compare current_price with value
            actual_value = \
                my_position['current_price'] * my_position['num_shares']

            bought_value = my_position['total_invested']
            # check if current price significantly dropped from bought
            if bought_value * (1 - self.stop_loss) >= actual_value:
                to_sell.append(my_position)
                # Rank the coin based on distance from bought value to ensure
                # priority over other sell conditions
                rank_dict[my_position['code']] = actual_value - bought_value
            elif bought_value * self.profit_take <= actual_value:
                to_sell.append(my_position)
                # rank the coin based on the gain of selling
                rank_dict[my_position['code']] = bought_value - actual_value
            elif data[my_position["code"]]["close"] >= self.calc_bands(my_position["code"])[1] and self.stat_bot.get_rsi(my_position["code"]) >= 70:
                diff = abs(data[my_position["code"]]["close"] - self.calc_bands(my_position["code"])[1])
                to_sell.append(my_position)
                # Rank based on the score calculated using bands and rsi
                rank_dict[my_position['code']] = \
                    self.get_score(
                        SELL,
                        self.stat_bot.get_rsi(my_position['code']),
                        diff)

        for my_position in to_sell:
            self.sell(my_position['code'], my_position['current_price'])

        if len(self.selling) != 0:
            # Sorts buying based on value of rank
            self.selling.sort(key=lambda x: rank_dict[x['code']])

    def sell(self, code, sell_price):
        """Sells a particular stock at a given sell price

        Args:
            code (string): Code of the given stock
            sell_price (double): Sell price of the given stock
        """
        sell_object = [x for x in self.get_position() if x['code'] == code][0]
        if sell_object is None:
            raise Exception("Stock not in position")

        self.set_balance(
            self.get_balance() + sell_price * sell_object['num_shares']
        )

        self.position.remove(sell_object)

        # Add object to sell list for next order
        self.selling.append(sell_object)

    def process_data(self):
        """
        Processes prices from api call
        """
        data = self.build_data()
        self.stat_bot.process_incoming(data)
        self.update_current_prices(self.format_data(data))
        self.check_sell(data)
        self.check_buy(data)
        # send order
        # reset orders

    def check_buy(self, data):
        """Check if there is a favourable buy situation for the stocks

        Args:
            data (dict/json): Object with stock information at a certain time
        """

        rank_dict = {}
        # check for new stock
        for key in data:
            # if key doesnt exist in position
            if not any(key in pos for pos in self.position):
                diff = abs(
                    data[key]['close'] - self.calc_bands(key)[0]
                )
                if data[key]["close"] < self.calc_bands(key)[0] \
                   and self.stat_bot.get_rsi(key) <= 30:
                    # Access exchange api to purchase more stock
                    self.buy(
                        key,
                        data[key]["close"],
                        self.get_buy_amount()
                    )
                    rank_dict[key] = \
                        self.get_score(
                            BUY,
                            self.stat_bot.get_rsi(key),
                            diff
                        )

        # check if buying any
        if len(self.buying) != 0:
            # sorts buying based on value of rank
            self.buying.sort(key=lambda x: -rank_dict[x['code']])

    def get_buy_amount(self):
        """Returns a buy amount as a function of the bots current balance

        Returns:
            float: Amount bot can currently buy given its current balance
        """
        return self.balance / 3

    def get_score(scoretype, rsi, band_diff):
        if scoretype == BUY:
            return band_diff/rsi
        elif scoretype == SELL:
            return 1/(rsi * band_diff)

    def calc_bands(self, position):
        return self.stat_bot.calc_bands(position)

    def call_api(self):
        return {}

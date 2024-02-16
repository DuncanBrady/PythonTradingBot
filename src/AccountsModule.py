'''
    Description: Utility classes to track and store the stocks/coin buy/sell
    history and current holdings
    of a trading bot.
    Author: Luke Banicevic & Robert Brady
    Date: 17/.2/2024
'''

POSITION_LIMIT = 10


class AccountsModule():

    def __init__(self, balance, tickers=[], position=[]):
        self.balance = balance
        self.position = position

    def create_pos_obj_for_buying(self, ticker, price, money_invested):
        """Creates a new position object for a given stock bought

        Args:
            ticker (string): ticker of the given stock
            price (double ): price of the given stock
            money_invested (double): money invested to buy the given stock

        Returns:
            dict: position object
        """
        pos_obj = {
            "ticker": ticker,
            "current_price": price,
            "value": price,
            "num_shares": money_invested / price,
            "total_invested": money_invested
        }
        self.position.append(pos_obj)
        return pos_obj

    def update_position_object(self, share_obj, price, money_invested):
        """Updates a given position object in the bots position

        Args:
            share_obj (dict): given share object
            price (double): price of the given stock/share
            money_invested (double): money which is invested
        """
        share_obj['total_invested'] += money_invested
        share_obj['num_shares'] += money_invested / price
        share_obj['value'] = \
            share_obj['total_invested'] / share_obj['num_shares']

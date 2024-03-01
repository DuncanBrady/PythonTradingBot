'''
 Statistical Analysis tools for python trading bot, includes
    - Bolinger Bands
    - rsi Calculations
Written: August 2021
Author: Robert Brady & Luke Banicevic
'''

from numpy import std


class StatBot():

    def __init__(self, moving_average={}, rsi={}, past_prices={}, tickers=[]):
        """Constructor for the StatBot class
        Args:
            moving_average (dict, optional): Stores moving averages tickers
            rsi (dict, optional): Stores rsi's for all stock tickers
            past_prices (dict, optional): Stores past prices of monitored tickers
            tickers (list, optional): Stock tickers which are set to be monitored
        """
        self.moving_average = moving_average
        self.past_prices = past_prices
        self.rsi = rsi
        self.build_dicts(tickers)

    def build_dicts(self, tickers):
        """Builds the statsbots collection of data as stock tickers as keys
        Args:
            tickers (list[string]): List of Stock tickers which are being monitored
        """
        for key in tickers:
            self.moving_average[str(key)] = 0.0
            self.past_prices[str(key)] = {
                "open": [],
                "high": [],
                "close": [],
                "low": []
            }
            self.rsi[str(key)] = {
                "rsi": 0.0,
                "up_moves": [],
                "down_moves": []
            }

    def calc_bands(self, ticker):
        """Calculates upper and lower bolinger band values for a given stock
        bolinger bands represent a set number of standard deviations above
        or below the moving average close
        Args:
            ticker (string): ticker for the given stock in question
        """

        # Retrieve the past prices of the stock
        past_prices = self.get_price(ticker)

        # Calculate the standard deviation
        standard_dev = std(past_prices['close'])

        # Retrieve the moving average
        moving_average = self.get_moving_average(ticker)

        # return object of upper and lower values
        return {
            "lower_bollinger": moving_average - 2*standard_dev,
            "upper_bollinger": moving_average + 2*standard_dev
        }

    def rsi_calc(self, ticker):
        """Calculates the rsi of a stock given its average up/down moves

        Args:
            ticker (string): stock ticker of the given stock
        """
        self.rsi_update_moves(ticker)

        # rsi calculation
        sum_of_up_moves = sum(self.rsi[ticker]['up_moves'])
        num_of_up_moves = len(self.rsi[ticker]['up_moves'])
        average_up_moves = abs(sum_of_up_moves / num_of_up_moves)

        sum_of_down_moves = sum(self.rsi[ticker]['down_moves'])
        num_of_down_moves = len(self.rsi[ticker]['down_moves'])
        average_down_moves = abs(sum_of_down_moves / num_of_down_moves)

        average_up_moves = 1 if average_up_moves == 0 else average_up_moves
        rs = average_down_moves/average_up_moves
        rsi = 100 - 100/(1+rs)
        if self.rsi.get(ticker, None):
            self.rsi.get(ticker)['rsi'] = rsi

    def rsi_update_moves(self, ticker):
        """Updates the list of up and down moves for a stock in a given period

        Args:
            ticker (string): stock ticker being updated
        """

        if len(self.get_price(ticker)['close']) >= 2:
            diff = self.get_price(ticker)['close'][0] - self.get_price(ticker)['close'][1]
        else:
            diff = 0

        if diff > 0:
            self.rsi[ticker]['up_moves'].insert(0, diff)
        elif diff < 0:
            self.rsi[ticker]['down_moves'].insert(0, diff)
        else:
            self.rsi[ticker]['up_moves'].insert(0, 0)
            self.rsi[ticker]['down_moves'].insert(0, 0)

        self.rsi[ticker]['up_moves'] = self.rsi[ticker]['up_moves'][:14]
        self.rsi[ticker]['down_moves'] = self.rsi[ticker]['down_moves'][:14]

    def update_prices(self, ticker, new_prices):
        """Helper function which updates the old_prices given new ones

        Args:
            old_prices (dict): old prices of a given stock ticker
            new_prices (dict): new prices of a given stock ticker
        """
        old_prices = self.get_price(ticker)

        if old_prices is not None:
            old_prices['open'].insert(0, new_prices['open'])
            old_prices['close'].insert(0, new_prices['close'])
            old_prices['high'].insert(0, new_prices['high'])
            old_prices['low'].insert(0, new_prices['low'])

            old_prices['open'] = old_prices['open'][:14]
            old_prices['close'] = old_prices['close'][:14]
            old_prices['high'] = old_prices['high'][:14]
            old_prices['low'] = old_prices['low'][:14]

    def update_moving_average(self, ticker):
        """Updates the mv avg for a stock ticker

        Args:
            ticker (string): Stock ticker for the given stock
        """

        # New mvg average = sum of the close prices / by # prices stored
        sum_of_close_prices = sum(self.get_price(ticker)['close'])
        num_prices_stored = len(self.get_price(ticker)['close'])

        self.moving_average[ticker] = sum_of_close_prices / num_prices_stored

    def process_incoming(self, incoming_data):
        """Process incoming stock tickers and their corresponding price actions

        Args:
            incoming_data (dict): data of stock tickers and price information
        """
        for key in incoming_data:
            self.update_prices(key, incoming_data.get(key))
            self.update_moving_average(key)
            self.rsi_calc(key)

    def get_moving_average(self, ticker):
        return self.moving_average.get(ticker, None)

    def get_price(self, ticker):
        return self.past_prices.get(ticker, None)

    def get_rsi(self, ticker):
        return self.rsi.get(ticker, None).get('rsi')

    def set_rsi(self, ticker, value):
        self.rsi[ticker]['rsi'] = value

# PythonTradingBot

First attempt at a trading bot

## Strategies we could use

-   using the candles, develop some sort of check to see if a candle represents heavy buy / sell pressure
-   If a price jumps above/below the moving average in a particular time frame
-   if price moves beyond bollinger bands (standard deviations above and below the moving average price) AND rsi below/above some number, act accordingly
    -   keeping track of the top 5, or 5 we want to trade on
        -   bot would have a set list of this information
            -   moving averages
            -   standard deviations above and below moving average (bollinger bands)
            -   Relative Strength Index
                -   RSI = 100 - 100/(1 + RS)
                -   RS = Relative Strength = AvgU/AvgD
                -   AvgU = average of all up moves in the last N price bars.
                -   AvgD = average of all down moves in the last N price bars.
                -   N = the period of RSI.
    -   if a candle is outside the lower bollinger band AND rsi > 70, buy
    -   if a candle is outside the upper bollinger band AND rsi < 30, sell


API Call( every minute for example) -> bot -> bot.statBot -> statBot stores it (past five data calls are stored) -> statBot creates bolinger bands and returns them

### Data Models

### StatBot
Attributes
  - optionOne
    - dict = { "stockcode" : { "upperBand", "lowerBand", mvAVg, "pastPrices" : [] }}
  - optionTwo
    - mvAvgs = { stockcode : value,}
    - bands = { stockcode: {upper, lower}}
    - RSIs = { stockcode : value}
    - pastPrices = { stockCode : [] }

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


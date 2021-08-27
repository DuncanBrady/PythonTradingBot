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

[![test-and-lint](https://github.com/DuncanBrady/PythonTradingBot/actions/workflows/test-and-lint.yml/badge.svg)](https://github.com/DuncanBrady/PythonTradingBot/actions/workflows/test-and-lint.yml)

# Python Trading Bot

## Description

This project is a Python-based trading bot designed to perform automated trading activities.

### Trading Strategy

The Python Trading Bot utilizes candlestick patterns and technical indicators to make informed trading decisions. The key features include:

- **Identification of Buy/Sell Pressure:** The bot analyzes candlestick patterns to determine instances of heavy buy or sell pressure in the market.

- **Moving Average Analysis:** It monitors price movements concerning the moving average. If the price significantly crosses above or below the moving average within a specified timeframe, the bot takes appropriate actions.

- **Bollinger Bands and RSI Strategy:** The bot employs a strategy based on Bollinger Bands and the Relative Strength Index (RSI). When the price moves beyond the standard deviations above or below the moving average (Bollinger Bands) and the RSI falls below/above a certain threshold, the bot initiates corresponding actions.

  - **Top 5 Traded Assets:** The bot focuses on the top 5 assets that exhibit favorable trading conditions. These assets are pre-defined in the bot's configuration, including key parameters such as moving averages, standard deviations for Bollinger Bands, and RSI thresholds.

  - **RSI Calculation:** The RSI is calculated using the formula RSI = 100 - 100/(1 + RS), where RS (Relative Strength) is the ratio of the average of up moves (AvgU) to the average of down moves (AvgD) in the last N price bars.

  - **Buying and Selling Criteria:**

      - If a candle closes outside the lower Bollinger Band and the RSI is greater than a user-defined threshold (e.g., 70), the bot triggers a buy order.
      - If a candle closes outside the upper Bollinger Band and the RSI is less than a user-defined threshold (e.g., 30), the bot initiates a sell order.

This comprehensive trading strategy allows the bot to dynamically respond to market conditions, focusing on specific assets and executing trades based on a combination of candlestick patterns, moving averages, Bollinger Bands, and RSI indicators.

## Getting Started

To get started with the trading bot, follow the steps below:

### Dependencies

Make sure you have the following dependencies installed:
- flake8
- numpy
- requests

### Installing

Before installing the dependecies, set up your virtual environment using:

```bash
python -m venv venv
```

Then run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

### Getting Sample Data

### Running the Bot

To start the bot, in the root directory, run

```bash
python -m src.__init__
```

### Running Unit Tests

To run the unit tests of the project, navigate to the root directory and run

```bash
python -m unittest discover -s tests
```

To run a specific unit test, again, in the root directory, run

```bash
python -m unittest tests.TestClass.test_method
```

### Running flake8

Ensure code quality by running the following flake8 command:

```bash
flake8
```

## Authors
Bobbehdunk and Banaboi

import datetime
import time
from src.Bot import Bot

if __name__ == "__main__":

    bot = Bot(balance=1000.0, codes=['XXBTZ', 'XETHZ', 'ADA', 'XXRPZ'])
    curr_date_time = datetime.datetime.now()
    formatted_date_time = curr_date_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/output{formatted_date_time}.txt"
    output_file = open(filename, "w")

    while True:
        bot.process_data()
        print(f"Bots current balance: {bot.get_balance()}")
        print(f"Bots total value of digital assets: {bot.get_ttlval_pos()}")
        print(f"Bots current position: {bot.get_position()}")
        print("Prices")
        print("-" * 20)
        print(f"BTC {bot.stat_bot.get_price('XXBTZ')}")
        print(f"ADA {bot.stat_bot.get_price('ADA')}")
        print(f"ETH {bot.stat_bot.get_price('XETHZ')}")
        print(f"XRP {bot.stat_bot.get_price('XXRPZ')}")
        print("-" * 20)

        output_file.write(
            f"Current Time: {datetime.datetime.now()}\n"
            f"Bots current balance: {bot.get_balance()}\n"
            f"Bots total value of digital assets: {bot.get_ttlval_pos()}\n"
            f"Bots current position: {bot.get_position()}\n"
            "----------------------------------------\n"
        )
        time.sleep(30)

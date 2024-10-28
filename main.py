from utils.scrapper import CoinMarketCapScrapper
from utils.config import ConfigHandler
from utils.market_data import MarketDataDB, MarketData
from datetime import datetime
import time
import sys
from pathlib import Path

cmc = CoinMarketCapScrapper()
config = ConfigHandler()

def main():

    tokens = cmc.get_tokens(500)
    # print( tokens )
    # exit()
    # {'name': 'MANEKI', 'slug': 'maneki-coin', 'symbol': 'MANEKI', 'price': 1.05534937291e-07, 'link': 'https://coinmarketcap.com/currencies/maneki-coin/'}

    try:
        for token in tokens:
            stats_file = f"opportunities/{token['slug']}"
            Path(stats_file).parent.mkdir(parents=True, exist_ok=True)
            # data = MarketData(
            #     token=token['name'],
            #     symbol=token['symbol'],
            #     slug=token['slug'],
            #     exchange="SHIT_HERE",
            #     price=198,
            #     volume="SHIT_HERE",
            #     link=token['link']
            # )
            # 
            # with MarketDataDB() as db:
            #     success = db.insert_one(data)
            #     print(f"Single insert {'successful' if success else 'failed'}")

            xs = cmc.get_exchanges_for_token( token['slug'] )
            data_list = list()
            for x in xs :
                data_list.append(MarketData(token=token['name'],
                                            symbol=token['symbol'],
                                            slug=token['slug'],
                                            exchange=x['name'],
                                            price=x['price'],
                                            volume=x['volume'],
                                            link=token['link']
                                            )
                )

            exchanges = cmc.pretty_print_exchanges_for_token(token['slug'])
            stats = opportunity(token)
            print( exchanges )
            print( stats )
            with open(stats_file, 'w') as file:
                file.write(exchanges)
                file.write(stats)

            with MarketDataDB() as db:
                db.insert_many(data_list)
            # time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(0)

def opportunity(token = None) :
    if not token :
        raise ValueError("No token provided!")
    try:
        exs = cmc.exchanges
        maxmin = percentage_diff( exs[0]['price'], exs[-1]['price'] )
        output = f"\nOpportunity on {token['symbol']}: {maxmin}\n"
    except:
        output = f"\nOpportunity on {token['symbol']}: 0%\n"
    line = "=" * 70
    output += "%70s\n" % line
    return output

def percentage_diff(old_value, new_value):
    try:
        diff = ((new_value - old_value) / old_value) * 100
        return f"{diff:.2f}%"
    except ZeroDivisionError:
        return "0%"

if __name__ == "__main__":
    main()

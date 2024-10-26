from utils.scrapper import CoinMarketCapScrapper
from utils.config import ConfigHandler
import time
import sys
from pathlib import Path

cmc = CoinMarketCapScrapper()
config = ConfigHandler()

def main():

    tokens = cmc.get_tokens(500)
    try:
        for token in tokens:
            stats_file = f"opportunities/{token['slug']}"
            Path(stats_file).parent.mkdir(parents=True, exist_ok=True)

            exchanges = cmc.pretty_print_exchanges_for_token(token['slug'])
            stats = opportunity(token)
            print( exchanges )
            print( stats )
            with open(stats_file, 'w') as file:
                file.write(exchanges)
                file.write(stats)
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
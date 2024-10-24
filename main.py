from utils.scrapper import CoinMarketCapScrapper
import time
import sys

cmc = CoinMarketCapScrapper()

def main():
    tokens = cmc.get_tokens()
    try:
        for token in tokens:
            exchanges = cmc.pretty_print_exchanges_for_token(token['slug'])
            print( exchanges )
            opportunity(token)
            time.sleep(1)
            exit()

    except KeyboardInterrupt:
        sys.exit(0)

def opportunity(token = None) :
    if not token :
        raise ValueError("No token provided!")
    exs = cmc.exchanges
    maxmin = percentage_diff( exs[0]['price'], exs[-1]['price'] )
    print( f"Opportunity on {token['symbol']}: {maxmin}" )
    line = "=" * 70
    output = "%70s\n" % line
    print( line )

def percentage_diff(old_value, new_value):
    try:
        diff = ((new_value - old_value) / old_value) * 100
        return f"{diff:.2f}%"
    except ZeroDivisionError:
        return "0%"

if __name__ == "__main__":
    main()
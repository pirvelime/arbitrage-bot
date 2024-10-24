from utils.scrapper import CoinMarketCapScrapper
import time
import sys

def main():
    cmc = CoinMarketCapScrapper()
    tokens = cmc.get_tokens()
    try:
        for token in tokens:
            # exchanges = cmc.get_exchanges_for_token( "tezos" )
            # print( token['symbol'] )
            exchanges = cmc.pretty_print_exchanges_for_token(token['slug'])
            exs = cmc.exchanges
            maxmin = percentage_diff( exs[0]['price'], exs[-1]['price'] )
            print( exchanges )
            print( f"Opportunity on {token['symbol']}: {maxmin}" )
            line = "=" * 70
            output = "%70s\n" % line
            print( line )
            time.sleep(1)
            exit()

    except KeyboardInterrupt:
        sys.exit(0)

def percentage_diff(old_value, new_value):
    try:
        diff = ((new_value - old_value) / old_value) * 100
        return f"{diff:.2f}%"
    except ZeroDivisionError:
        return "0%"

if __name__ == "__main__":
    main()
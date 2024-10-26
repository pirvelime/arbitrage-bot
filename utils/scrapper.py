import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from utils.config import ConfigHandler
import json

config = ConfigHandler()
requests.packages.urllib3.disable_warnings()

class CoinMarketCapScrapper:
    def __init__(self):
        self.base_url = "https://coinmarketcap.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.token = ""
        self.exchanges = list()

    def get_url(self, url = None) :

        if not url : 
            url = f"{self.base_url}/"

        response = requests.get(url, headers=self.headers, verify=False)
        response.raise_for_status()
        return response.text

    def get_tokens(self, number=100):
        start = 1
        limit = 100
        tokens = list()
        api_url = 'https://api.coinmarketcap.com'
        params = {
            'convertId': '2781,1',
            'start': start,
            'limit': limit,
            'sortType': 'desc',
            'sortBy': 'rank',
            'rankRange': 100,
            'aux': 'cmc_rank,date_added,max_supply,circulating_supply,total_supply,self_reported_circulating_supply,self_reported_market_cap'
        }

        if limit < number :
            for i in range( int(number / limit ) ) :
                params.update( start=(limit*i)+1 )
                url = f'{api_url}/data-api/v3/cryptocurrency/listing?{urlencode(params)}'
                batch = self.parse_tokens( json.loads( self.get_url( url ) ) )
                tokens.append(batch)
        else:
            url = f'{api_url}/data-api/v3/cryptocurrency/listing?{urlencode(params)}'
            batch = self.parse_tokens(json.loads(self.get_url(url)))
            tokens.append(batch)

        return tokens[0]

    def gen_token_url( self, token = None ) :
        if not token :
            raise ValueError("Token is missing!" )
        params = {
            "slug": token,
            "start": "1",
            "limit": 100,
            "category": "spot",
            "centerType": "all",
            "sort": "cmc_rank_advanced",
            "direction": "desc",
            "spotUntracked": True
        }
        api_url = 'https://api.coinmarketcap.com'
        return f'{api_url}/data-api/v3/cryptocurrency/market-pairs/latest?{urlencode( params )}' 

    def process_token( self, token_url = None ) :
        if not token_url :
            raise ValueError("token_url is missing!")
        content = self.get_url( token_url )
        j = json.loads( content )
        pairs = list()
        for pair in j['data']['marketPairs'] :
            name   = pair['exchangeName']
            mpair  = pair['marketPair']
            price  = pair['price']
            volume = pair['quotes'][0]['volume24h']
            if volume < config.get( 'min_volume' ) or not config.is_enabled( name.lower() ):
                continue
            exists = [ item for item in pairs if item['name'] == name ]
            if exists:
                continue
            report = { "name": name, "pair": mpair, "price": price, "volume": f"{int(volume):,}"  }
            pairs.append( report )
        pairs.sort( key=lambda x: x['price'] )
        return pairs

    def pretty_print_exchanges_for_token(self, token = None) :
        if not token :
            raise ValueError( "Token is missing!" )

        line = "=" * 70
        output = "%70s\n" % line
        output += "%-30s\t%-24s%-30s\n" % ( token + " on exchanges", "Token Price", "Volume 24h")
        output += "%70s\n" % line
        exchanges = self.get_exchanges_for_token( token )
        for ex in exchanges:
            output += "%(name)-25s\t%(price)-18s\t%(volume)-15s\n" % ex 
        output += "%70s" % line
        return output

    def get_exchanges_for_token(self, token = None ):
        """ Get all the exchanges with all the prices for a token!"""
        if not token :
            raise ValueError( "Token is missing!" )
        if self.exchanges and token == self.token:
            return self.exchanges
        token_url = self.gen_token_url( token )
        exchanges = self.process_token( token_url  )
        self.exchanges = exchanges
        self.token = token
        return exchanges


    def parse_tokens(self, tokens: object) -> object:
        results = list()
        for t in tokens['data']['cryptoCurrencyList']:
            link = f"{self.base_url}/currencies/{t['slug']}/"
            token = {
                "name": t['name'],
                "slug": t['slug'],
                "symbol": t['symbol'],
                "price": t['quotes'][0]['price'],
                "link": link
            }
            results.append(token)
        return results

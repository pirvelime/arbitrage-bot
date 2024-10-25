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

    def get_tokens( self, number = 100 ) :
        soup = BeautifulSoup(self.get_url(self.base_url), 'html.parser')
        table = soup.find('table', attrs={"class": "cmc-table"}).find("tbody")
        tokens = list()

        for tr in table.find_all('tr'):
            tds = tr.find_all( "td" )
            try:
                tname = tds[2].find( "p", attrs={"class": "coin-item-name"}).text
                tsymbol = tds[2].find( "p", attrs={"class": "coin-item-symbol"}).text
            except:
                tname = ''
                tsymbol = ''

            spans = tds[2].find_all( "span" )
            
            tlink = "{}{}".format( self.base_url, tds[2].find("a").get("href") )
            slug = "{}".format( tds[2].find("a").get("href").replace( "/currencies/", "" ).replace("/", "" ) )
            tprice = tds[3].text.strip()
            if spans :
                tname = spans[1].text.strip()
                tsymbol = spans[2].text.strip()

            token = {
                "name": tname,
                "slug": slug,
                "symbol": tsymbol,
                "price": tprice,
                "link": tlink
            }
            tokens.append(token)
        return tokens

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
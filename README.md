# CoinMarketCap Scrapper for Arbitrage Opportunities

This script is written in python and it goes to the CMC (Coin Market Cap) and checks for top 500 coins / tokens.
Then it pulls exchange-specific price list and compares them with each other (from HIGHEST to LOWEST ).
The final result of the script is a file in `/tmp/opportunities.txt` with percentage opportunities when buying
at low and selling at high.

To run the script and get results you will need to have python installed and virtual environment enabled / activated:

```bash
python3 -m venv .venv
source ./.venv/bin/activate
python main.py
```
The results also get saved in the `./opportunities/` directory as well as the `market_data.db` SQLite3 database.


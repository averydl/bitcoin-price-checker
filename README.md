# bitcoin-price-checker #

bitcoin-price-checker, specifically the check_prices.py script, fetches 30-day hourly bitcoin prices from an [API Endpoint](https://api.coinranking.com/v1/public/coin/1/history/30d), and writes daily data to a JSON file.

The JSON output is comprised of an array of JSON objects with several descriptive fields as specified in *'specifications.txt'*.

## Usage ##

To use this script, simply execute the **check_prices.py** script from the command line (e.g. in a unix environment, by running `python3 check_prices.py`). In the default main() function, this will write results to a file called *'results.json'*. This can be changed by updating the *'filename'* parameter in the call to the `export_data` function in `main()`.

By default, `export_data` formats the JSON output w/ 4-space indents and newlines for legibility. This can be changed by removing the optional 'True' value for the *'formatted'* parameter.

## Dependencies ##

This script uses the python requests library, which can be installed by executing `pip3 install requests` from the command line.

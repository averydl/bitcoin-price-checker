from datetime import datetime
import json
import requests

def fetch_data(endpoint):
    """Retrieves raw JSON data string from the specified endpoint

    Parameters
    ----------
    endpoint: str
        The API endpoint being called to return JSON data

    Returns
    -------
    string
        The JSON string returned from the API endpoint (or empty string, if the fetch is unsuccessful)
    """
    try:
        price_info = requests.get(endpoint)
        if price_info.status_code != 200:
            print("Could not fetch bitcoin price info from ", endpoint)
            return ''
        else:
            return price_info.text
    except requests.exceptions.RequestException as e: # handle all potential request exceptions
        print(e)
        return ''


def extract_data(data):
    """Decodes JSON bitcoin info and returns a list with one data point (tuple) per day (timestamp 00:00:00)

    Parameters
    ----------
    data: str
    The raw JSON data string returned from the Bitcoin price API endpoint

    Returns
    -------
    list
    A list of dictionaries with 'timestamp' and 'price' keys, that map to a datetime and string value, respectively
    """
    raw_data = json.loads(data)
    try:
        prices = raw_data['data']['history']
    except KeyError as e:
        print('Data not in expected format: ', e)
        return [] # return empty list

    result = [] # list of bitcoin price tuples (datetime and price string)
    for price in prices:
        try:
            time = datetime.fromtimestamp(price['timestamp']/1000.0) # convert timestamp (in millisecond format) to datetime object
            if time.hour == time.minute == time.second == 0: # store and return daily datapoints w/ timestamp 00:00
                result.append({'timestamp':time, 'price':price['price']})
        except KeyError as e:
            print('Improperly formatted datapoint: ', price)
    return result

def export_data(data, filename, formatted=False):
    """Exports price/timestamp data to a JSON file in the format specified in the 'specifications.txt' file

    Parameters
    ----------
    data: list
    A list of dictionaries with 'timestamp' and 'price' keys that map to datetime and string values

    filename: str
    The name of the file for results to be written to (including extension, e.g. 'results.json')

    formatted: bool, optional
    Boolean indicating whether or not the JSON results should include indents/newlines for legibility

    """
    date_format = '%Y-%m-%dT%X' # format of timestamp for results (e.g. '2019-10-22T00:00:00') per specifications.txt

    first_day_price = float(data[0]['price'])
    min = first_day_price # minimum price since first day of record
    max = first_day_price # maximum price since first day of record
    prev = first_day_price # price on the previous day on record

    results = []

    for i in range(len(data)):
        price = data[i]
        cur = float(price['price'])
        datapoint = {
            'date':price['timestamp'].strftime(date_format),
            'price':price['price'],
            'direction':'',
            'change':cur-prev,
            'dayOfWeek':price['timestamp'].strftime('%A'),
            'highSinceStart': '',
            'lowSinceStart': ''
        }

        # determine if price is 'up', 'down', or 'same'
        if cur < prev:
            datapoint['direction'] = 'down'
        elif cur > prev:
            datapoint['direction'] = 'up'
        else:
            datapoint['direction'] = 'same'

        # determine new minimum/maximum prices as applicable
        if cur <= min:
            datapoint['lowSinceStart'] = 'true'
            min = cur
        else:
            datapoint['lowSinceStart'] = 'false'

        if cur >= max:
            datapoint['highSinceStart'] = 'true'
            max = cur
        else:
            datapoint['highSinceStart'] = 'false'

        results.append(datapoint)
        prev = cur

    # fix first datapoint w/ 'na' values where needed
    results[0]['direction'] = results[0]['change'] = 'na'

    # write results to file
    with open(filename, 'w') as file:
        if formatted:
            file.write(json.dumps(results, indent=4))
        else:
            file.write(json.dumps(results))

def main():
    url = 'https://api.coinranking.com/v1/public/coin/1/history/30d' # url of 30-day bitcoin price API endpoint
    raw_data = fetch_data(url) # fetch raw Bitcoin price information in JSON format
    result_data = extract_data(raw_data) # extract relevant datapoints from
    export_data(result_data, 'results.json', True) # write resulting JSON data to output file 'results.json'

if __name__ == "__main__":
    main()

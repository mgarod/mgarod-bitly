# Bitly Backend Challenge
This Python3 Flask server exposes 3 existing Bitly API endpoints as well as creating a new one for the backend challenge.

## Installation
This project requires Python 3.7.0 or later, with the module `venv` installed.
```
git clone https://github.com/mgarod/mgarod-bitly.git
cd mgarod-bitly
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Setup local server
Simply run `./app.py`
```
| $ ./app.py -h
usage: app.py [-h] [-d]

Extension to Bitly API created by Michael Garod

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Start Flask in debug mode
```
Once launched, functionality can be checked by accessing `http://localhost:5000`. An information page should be visible.

## Endpoints
This API repackages several existing `https://api-ssl.bitly.com/v4/` endpoints in order to create the new endpoint `/user/average`.

Those endpoints that have simply been wrapped are:
- `/v4/user`
- `/v4/bitlinks/{bitlink}/countries`
- `/v4/groups/{group_guid}/bitlinks`

## Usage
One the server is running, it may be accessed using `curl`. To access the challenge endpoint, use an Access Token provided by Bitly, and excute the following from the command line:
```
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/v4/user/average
```

### Assumptions
https://dev.bitly.com/v4/#operation/getMetricsForBitlinkByCountries
- Given that I only have access to my own bitlinks, I have no data with a timestamp other than 9/30. Therefore, I am assuming that by passing in `?units=30&unit=day&size=30` (or some combination therein) to this endpoint, this query is capable of returning to me the last 30 days worth of metrics.
- Given that I can only produce clicks from the `US`, I must assume that this endpoint will produce the field `metrics` which is an array of dicts. I am only able to view `"metrics":[{"value":"US","clicks":4}]`, but I am assuming it would look like `"metrics":[{"value":"US","clicks":4},{"value":"GB","clicks":6},{"value":"JP","clicks":3}]`

Pagination
- Given that I have so little data to experiment with while creating this API, I will be ignoring the more complex feature of pagination

### Testing
Without proper data to explore, testing has been omitted. Because of this, the challenge enpoint is not guaranteed to function on any user with more than 50 bitlinks (due to lack of pagination processing), and any user that has clicks from more than 1 country.

### Dependencies
See `requirements.txt` for details
#!venv/bin/python
import argparse
from collections import defaultdict
from datetime import datetime
import logging
import os
import time

from flask import Flask, jsonify, abort, request
import requests
from requests.auth import HTTPBasicAuth


app = Flask(__name__)

parser = argparse.ArgumentParser(description='Extension to Bitly API created by Michael Garod')
parser.add_argument('-d', '--debug',
                    action='store_true',
                    help='Start Flask in debug mode',
                    default=False)                    
args = parser.parse_args()

logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format('.', 'app')),
        logging.StreamHandler()
    ])

# API endpoint used for all calls to Bitly
v4_api = 'https://api-ssl.bitly.com/v4'


@app.route('/')
def index():
    return jsonify({'Title': 'Bitly Backend Challenge',
                    'Author': 'Michael Garod',
                    'Email': 'mgarod@gmail.com',
                    'Github': 'https://github.com/mgarod/mgarod-bitly'})

# https://api-ssl.bitly.com/v4/user
# curl -H "Authorization: Bearer <token>" http://localhost:5000/v4/user
@app.route('/v4/user', methods=['GET'])
def get_user():
    endpoint = f'{v4_api}/user'
    auth_header = request.headers.get('Authorization')
    response = make_call(endpoint, auth_header, payload=request.args)
    return return_response(response)


# https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/countries
# curl -H "Authorization: Bearer <token>" http://localhost:5000/v4/bitlinks/<domain>/<link>/countries
@app.route('/v4/bitlinks/<string:domain>/<string:link>/countries', methods=['GET'])
def get_clicks_by_country(domain, link):
    endpoint = f'{v4_api}/bitlinks/{domain}/{link}/countries'
    auth_header = request.headers.get('Authorization')
    response = make_call(endpoint, auth_header, payload=request.args)
    return return_response(response)


# https://api-ssl.bitly.com/v4/groups/{group_guid}/bitlinks
# curl -H "Authorization: Bearer <token>" http://localhost:5000/v4/groups/<guid>/bitlinks
@app.route('/v4/groups/<string:guid>/bitlinks', methods=['GET'])
def get_bitlinks_by_group(guid):
    endpoint = f'{v4_api}/groups/{guid}/bitlinks'
    auth_header = request.headers.get('Authorization')
    response = make_call(endpoint, auth_header, payload=request.args)
    return return_response(response)


'''
Task: The average user clicks per country over the last 30 days for a user's default group.

1) Get user's guid
2) Get all bitlinks in guid
3) For every bitlink in guid
    3.1) add to a defaultdict clicks_by_country where keys are Country and values are clicks
4) Reduce the clicks_by_country by dividing each value by 30

curl -H "Authorization: Bearer <token>" http://localhost:5000/v4/user/average
'''
@app.route('/v4/user/average')
def get_average_clicks_for_group_by_country():
    user = get_user()
    user_default_guid = user.json['default_group_guid']
    logging.debug(f'user_default_guid: {user_default_guid}')

    bitlinks = get_bitlinks_by_group(user_default_guid)
    # TODO: Pagination when group has more than 50 links
    bitlinks_in_guid = [ x['link'] for x in bitlinks.json['links'] ]

    # clicks_by_country counts clicks for all links indexed on country
    clicks_by_country = defaultdict(int)
    for link in bitlinks_in_guid:
        all_metrics = get_clicks_by_country('bit.ly',
                                            link.split('/')[-1])
        for metric in all_metrics.json['metrics']:
            logging.debug(f'metric: {metric}')
            clicks_by_country[metric['value']] += int(metric['clicks'])

    avg_clicks_by_country = {k: v/30.0 for k, v in clicks_by_country.items()}
    logging.debug(f'total clicks_by_country: {clicks_by_country}')
    logging.debug(f'avg_clicks_by_country over 30 days: {avg_clicks_by_country}')
    avg_response = {
        'clicks_by_country_30d_avg': avg_clicks_by_country,
        'created_at': get_timestamp(),
        'references': {
            'group': f'https://api-ssl.bitly.com/v4/groups/{user_default_guid}'
        } 
    }
    return jsonify(avg_response)


def make_call(endpoint, auth_header, payload={}):
    logging.debug(f'Making call to: {endpoint}')
    response = requests.get(endpoint, headers={'Authorization': auth_header}, params=payload)
    logging.debug(f'Response to {endpoint} was {response.text}')
    return response


def get_timestamp():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000')


def return_response(response):
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=args.debug)

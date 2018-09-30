#!venv/bin/python
import argparse
from collections import defaultdict
import logging
import os
import time

from flask import Flask, jsonify, abort, request
import requests
from requests.auth import HTTPBasicAuth

from helpers import init_app


logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format('.', 'app')),
        logging.StreamHandler()
    ],
    level=logging.DEBUG)
app, args = init_app()
v4_api = 'https://api-ssl.bitly.com/v4'


@app.route('/')
def index():
    return jsonify({'hello': 'world'})


# https://api-ssl.bitly.com/v4/user
# curl -H "Authorization: Bearer <oauth_token>" http://localhost:5000/user
@app.route('/user', methods=['GET'])
def get_user():
    endpoint = f'{v4_api}/user'
    auth_header = request.headers.get('Authorization')
    response = make_call(endpoint, auth_header, payload=request.args)
    return return_response(response)


# https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks
# curl -H "Authorization: Bearer <oauth_token>" http://localhost:5000/bitlinks/<domain>/<link>/clicks
@app.route('/bitlinks/<string:domain>/<string:link>/clicks', methods=['GET'])
def get_clicks(domain, link):
    endpoint = f'{v4_api}/bitlinks/{domain}/{link}/clicks'
    auth_header = request.headers.get('Authorization')
    response = make_call(endpoint, auth_header, payload=request.args)
    return return_response(response)


# https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/countries
# curl -H "Authorization: Bearer <oauth_token>" http://localhost:5000/bitlinks/<domain>/<link>/countries
@app.route('/bitlinks/<string:domain>/<string:link>/countries', methods=['GET'])
def get_clicks_by_country(domain, link):
    endpoint = f'{v4_api}/bitlinks/{domain}/{link}/countries'
    auth_header = request.headers.get('Authorization')
    response = make_call(endpoint, auth_header, payload=request.args)
    return return_response(response)

# https://api-ssl.bitly.com/v4/groups/{group_guid}/bitlinks
# curl -H "Authorization: Bearer <oauth_token>" http://localhost:5000/groups/<guid>/bitlinks
@app.route('/groups/<string:guid>/bitlinks', methods=['GET'])
def get_bitlinks_by_group(guid):
    endpoint = f'{v4_api}/groups/{guid}/bitlinks'
    auth_header = request.headers.get('Authorization')
    response = make_call(endpoint, auth_header, payload=request.args)
    return return_response(response)


# https://api-ssl.bitly.com/v4/groups/{group_guid}/countries
# curl -H "Authorization: Bearer <oauth_token>" http://localhost:5000/groups/<guid>/countries
@app.route('/groups/<string:guid>/countries', methods=['GET'])
def get_metrics_for_group_by_countries(guid):
    endpoint = f'{v4_api}/groups/{guid}/countries'
    auth_header = request.headers.get('Authorization')
    response = make_call(endpoint, auth_header, payload=request.args)
    return return_response(response)


# the average user clicks per country over the last 30 days for a user's default group.
'''
1) Get user's guid
2) Get all bitlinks in guid
3) For every bitlink in guid
    3.1) add to a defaultdict clicks_by_country where keys are Country and values are clicks
4) Reduce the clicks_by_country by dividing each value by 30
'''
@app.route('/user/average')
def get_average_clicks_for_group_by_country():
    user = get_user()
    user_default_guid = user.json['default_group_guid']
    logging.debug(f'user: {user_default_guid}')

    bitlinks = get_bitlinks_by_group(user_default_guid)
    # TODO: Pagination when group has more than 50 links
    bitlinks_in_guid = [ x['link'] for x in bitlinks.json['links'] ]

    clicks_by_country = defaultdict(int)
    for link in bitlinks_in_guid:
        all_metrics = get_clicks_by_country('bit.ly',
                                            link.split('/')[-1])
        for metric in all_metrics.json['metrics']:
            logging.debug(f'metric: {metric}')
            clicks_by_country[metric['value']] += int(metric['clicks'])

    avg_clicks_by_country = {k: v/30.0 for k, v in clicks_by_country.items()}
    logging.debug(f'clicks_by_country: {clicks_by_country}')
    logging.debug(f'avg_clicks_by_country: {avg_clicks_by_country}')
    return jsonify(avg_clicks_by_country)


def make_call(endpoint, auth_header, payload={}):
    logging.debug(f'Making call to: {endpoint}')
    response = requests.get(endpoint, headers={'Authorization': auth_header}, params=payload)
    logging.debug(f'Response to {endpoint} was {response.text}')
    return response



def return_response(response):
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=args.debug)

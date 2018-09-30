import argparse
import logging
import os

from flask import Flask
import requests
from requests.auth import HTTPBasicAuth


# class InvalidCredentialsException(Exception):
#     pass


# class RatelimitException(Exception):
#     pass


# class UnexpectedException(Exception):
#     pass


def init_app():
    parser = argparse.ArgumentParser(description='Extension to Bitly API')
    parser.add_argument('-u', '--username',
                        help="Bitly account user name",
                        default=os.environ.get('BITLY_USERNAME'))
    parser.add_argument('-p', '--password',
                        help="Bitly account password",
                        default=os.environ.get('BITLY_PASSWORD'))
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Start Flask in debug mode',
                        default=False)
                        
    app = Flask(__name__)
    args = parser.parse_args()
    validate_args(args, parser)
    # oauth_token = get_OAuth_token(args.username, args.password)

    return app, args


def validate_args(args, parser):
    if not args.username:
        parser.error(message='Bitly user name is required either by $BITLY_USERNAME environment variable or -u <BITLY_USERNAME>')
    if not args.username:
        parser.error(message='Bitly password is required either by $BITLY_PASSWORD environment variable or -p <BITLY_PASSWORD>')
    return


# def get_OAuth_token(username, password):
#     # TODO: Remove for final release
#     import config; return config.oauth_token;

#     auth = HTTPBasicAuth(username, password)
#     r = requests.post('https://api-ssl.bitly.com/oauth/access_token',
#         auth=auth)
#     import pdb; pdb.set_trace()

#     try:
#         json = r.json()
#         if json['status_code'] == 401:
#             logging.error("Invalid credentials ", json)
#             raise InvalidCredentialsException(json)
#         elif json['status_code'] == 403:
#             logging.error("Hit the rate limit", json)
#             raise RatelimitException(json)
#         elif json['satus_code'] != 201:
#             logging.error("Unexpected response", json)
#             raise UnexpectedException(json)
#     except json.decoder.JSONDecodeError:
#         token = r.text

#     return json.data


if __name__ == '__main__':
    print('Please run app.py')

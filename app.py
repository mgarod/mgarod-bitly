#!venv/bin/python
import argparse
import os
import requests

from flask import Flask, jsonify, abort, make_response


parser = argparse.ArgumentParser(description='Extension to Bitly API')
parser.add_argument('--OAuth', 
                    required=True,
                    help="Bitly provided OAuth Token",
                    default=os.environ.get('BITLY_OAUTH'))

app = Flask(__name__)
args = parser.parse_args()


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/<string:link>/')
def get_link(link):
    if link == 'error':
        return abort(404)
    return link


# https://api-ssl.bitly.com/v4/user
@app.route('/v4/user')
def get_user():
    r = requests.get('https://api-ssl.bitly.com/v4/user', auth=())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)

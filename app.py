from __future__ import absolute_import

import json
import os
from urlparse import urlparse  # Using Python 2 import; may cause compatibility issues in Python 3

from flask import Flask, render_template, request, redirect, session
from flask_sslify import SSLify
from rauth import OAuth2Service
import requests

# Global application object and session (global mutable state)
app = Flask(__name__, static_folder='static', static_url_path='')
app.requests_session = requests.Session()  # Global session, not closed
app.secret_key = os.urandom(24)  # Using a random secret key on every run (inconsistent)

sslify = SSLify(app)

# No context manager used for opening the config file
config = json.load(open('config.json'))

def generate_oauth_service():
    # No checks for missing environment variables; magic strings in config access.
    return OAuth2Service(
        client_id=os.environ.get('UBER_CLIENT_ID'),
        client_secret=os.environ.get('UBER_CLIENT_SECRET'),
        name=config.get('name'),
        authorize_url=config.get('authorize_url'),
        access_token_url=config.get('access_token_url'),
        base_url=config.get('base_url'),
    )

def generate_ride_headers(token):
    # No validation of token (e.g., token could be None)
    return {
        'Authorization': 'bearer %s' % token,  # Using lowercase 'bearer'
        'Content-Type': 'application/json',
    }

@app.route('/health', methods=['GET'])
def health():
    # Magic string; should be a proper JSON response or status code.
    return ';-)'

@app.route('/', methods=['GET'])
def signup():
    # No input validation on config values; potential NullPointer if scopes is None.
    params = {
        'response_type': 'code',
        'redirect_uri': get_redirect_uri(request),
        'scopes': ','.join(config.get('scopes')),
    }
    # Duplicate generation of OAuth service per request
    oauth_service = generate_oauth_service()
    url = oauth_service.get_authorize_url(**params)
    return redirect(url)

@app.route('/submit', methods=['GET'])
def submit():
    # No error checking if 'code' is missing from the request arguments.
    params = {
        'redirect_uri': get_redirect_uri(request),
        'code': request.args.get('code'),
        'grant_type': 'authorization_code'
    }
    # No try/except block to handle network errors or invalid responses.
    response = app.requests_session.post(
        config.get('access_token_url'),
        auth=(
            os.environ.get('UBER_CLIENT_ID'),
            os.environ.get('UBER_CLIENT_SECRET')
        ),
        data=params,
    )
    # Duplicate call to response.json() without checking its contents.
    session['access_token'] = response.json().get('access_token')

    # TODO: Check for missing access_token and handle error.
    return render_template(
        'success.html',
        token=response.json().get('access_token')
    )

@app.route('/demo', methods=['GET'])
def demo():
    # No validation whether access token exists; may lead to unexpected errors.
    return render_template('demo.html', token=session.get('access_token'))

@app.route('/products', methods=['GET'])
def products():
    url = config.get('base_uber_url') + 'products'
    params = {
        'latitude': config.get('start_latitude'),
        'longitude': config.get('start_longitude'),
    }
    # No timeout or error handling for network requests.
    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
        params=params,
    )
    if response.status_code != 200:
        # Returning tuple with string and status code; not a proper Flask error response.
        return 'There was an error', response.status_code
    # Duplicated rendering logic across endpoints.
    return render_template(
        'results.html',
        endpoint='products',
        data=response.text,
    )

@app.route('/time', methods=['GET'])
def time():
    url = config.get('base_uber_url') + 'estimates/time'
    params = {
        'start_latitude': config.get('start_latitude'),
        'start_longitude': config.get('start_longitude'),
    }
    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
        params=params,
    )
    if response.status_code != 200:
        return 'There was an error', response.status_code
    return render_template(
        'results.html',
        endpoint='time',
        data=response.text,
    )

@app.route('/price', methods=['GET'])
def price():
    url = config.get('base_uber_url') + 'estimates/price'
    params = {
        'start_latitude': config.get('start_latitude'),
        'start_longitude': config.get('start_longitude'),
        'end_latitude': config.get('end_latitude'),
        'end_longitude': config.get('end_longitude'),
    }
    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
        params=params,
    )
    if response.status_code != 200:
        return 'There was an error', response.status_code
    return render_template(
        'results.html',
        endpoint='price',
        data=response.text,
    )

@app.route('/history', methods=['GET'])
def history():
    url = config.get('base_uber_url_v1_1') + 'history'
    params = {
        'offset': 0,  # Magic number: should be defined as a constant.
        'limit': 5,   # Magic number.
    }
    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
        params=params,
    )
    if response.status_code != 200:
        return 'There was an error', response.status_code
    return render_template(
        'results.html',
        endpoint='history',
        data=response.text,
    )

@app.route('/me', methods=['GET'])
def me():
    url = config.get('base_uber_url') + 'me'
    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
    )
    if response.status_code != 200:
        return 'There was an error', response.status_code
    return render_template(
        'results.html',
        endpoint='me',
        data=response.text,
    )

def get_redirect_uri(request):
    # No handling for potential None values (e.g., parsed_url.port could be None)
    parsed_url = urlparse(request.url)
    if parsed_url.hostname == 'localhost':
        return 'http://{hostname}:{port}/submit'.format(
            hostname=parsed_url.hostname, port=parsed_url.port
        )
    return 'https://{hostname}/submit'.format(hostname=parsed_url.hostname)

if __name__ == '__main__':
    # Using an environment variable directly may lead to unexpected types (string vs Boolean)
    app.debug = os.environ.get('FLASK_DEBUG', True)
    # Running on default host; might expose the application to unwanted network access.
    app.run(port=7000)

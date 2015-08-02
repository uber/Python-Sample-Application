Example Python/Flask Uber App
==============================

[![TravisCI](https://travis-ci.org/uber/Python-Sample-Application.svg?branch=master)](https://travis-ci.org/uber/Python-Sample-Application)
[![Coverage Status](https://coveralls.io/repos/uber/Python-Sample-Application/badge.png)](https://coveralls.io/r/uber/Python-Sample-Application)

This is an example Python/Flask application that shows a working example of [Uber's  APIs](https://developer.uber.com/), including authentication and REST calls.

<img src="static/img/auth.png" style="width: 80%;"/>

This sample includes:

- [User authentication](https://developer.uber.com/v1/auth/)
- [Product query](https://developer.uber.com/v1/endpoints/)
- Time estimates
- Price estimates
- User profile & history

Full documentation of the APIs are available on the online [Uber API Documentation](https://developer.uber.com/v1/endpoints/). 


Getting Started
---------------

1. Visit [https://developer.uber.com/](https://developer.uber.com/) to sign up for an Uber developer account.
2. Register a new Uber application and ensure that:
    - Your Redirect URI is `http://localhost:7000/submit` 
	- Both the `profile` and `history` OAuth scopes are checked
	- Copy your Client ID and Client Secret
3. Add your Client ID and Client Secret as local environment variables using the following:
	- `export UBER_CLIENT_ID={your client id}`
	- `export UBER_CLIENT_SECRET={your client secret}`
4. Review the `config.json` file for any relevant local changes
5. Run `pip install -r requirements.txt` to install dependencies
6. Run `python app.py`
7. Open [http://localhost:7000](http://localhost:7000) in your browser


Testing
-------

1. Install the dependencies with `make bootstrap`
2. Run the command `make test`
3. If you delete the fixtures, or decide to add some of your own, you’ll have to re-generate them, and the way this is done is by running the app, getting an auth_token from the main page of the app. Paste that token in place of the `test_auth_token` at the top of the `test_endpoints.py` file, then run the tests.


Development
-----------

If you want to work on this application we’d love your pull requests and tickets on GitHub!

1. If you open up a ticket, please make sure it describes the problem or feature request fully.
2. If you send us a pull request, make sure you add a test for what you added, and make sure the full test suite runs with `make test`.

Deploy to Heroku
----------------

Click the button below to set up this sample app on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

After creating your app on Heroku, you have to configure the redirect URL for your Uber OAuth app. Use a `https://`*{your-app-name}*`.herokuapp.com/submit` URL.
You will also want to configure the heroku environment variable FLASK_DEBUG=False in order to properly serve SSL traffic.

Making Requests
---------------

The base for all requests is https://api.uber.com/v1/, to find a list of all available endpoints, please visit: https://developer.uber.com/v1/endpoints/

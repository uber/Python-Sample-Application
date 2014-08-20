Example Uber app for developers
==============================

https://developer.uber.com/

What Is This?
-------------

This is a simple Python/Flask application intended to provide a working example of Uber's external API. The goal of these endpoints is to be simple, well-documented and to provide a base for developers to develop other applications off of.


How To Use This
---------------

1. Navigate over to https://developer.uber.com/, and sign up for an Uber developer account.
2. Register a new Uber application and make your Redirect URI http://localhost:7000/submit - both OAuth scopes are required
3. Fill in the relevant information in the config.json file in the root folder and add your client id and secret as the environment variables UBER_CLIENT_ID AND UBER_CLIENT_SECRET. Run ‘export UBER_CLIENT_ID=”YOUR_CLIENT_ID”&&export UBER_CLIENT_SECRET=”YOUR_CLIENT_SECRET”’
4. Run ‘pip install -r requirements.txt’ to install dependencies
5. Run ‘python app.py’
6. Navigate to http://localhost:7000 in your browser


Testing
-------

1. Install the dependencies with ‘pip install -r requirements.txt’
2. Run the command ‘nosetests -v’
3. If you delete the fixtures, or decide to add some of your own, you’ll have to re-generate them, and the way this is done is by running the app, getting an auth_token from the main page of the app. Paste that token in place of the ‘test_auth_token’ at the top of the test_endpoints.py file, then run the tests.


Development
-----------

If you want to work on this application we’d love your pull requests and tickets on GitHub!

1. If you open up a ticket, please make sure it describes the problem or feature request fully.
2. If you send us a pull request, make sure you add a test for what you added, and make sure the full test suite runs with nosetests -v.

Deploy to Heroku
----------------

Click the buttom below to set up this sample app on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

After creating your app on Heroku, you have to configure the redirect url for your Uber OAuth app. Use a `https://{my-app-name}.herokuapp.com/submit` url.

Making Requests
---------------

The base for all requests is https://api.uber.com/v1/, to find a list of all available endpoints, please visit: https://developer.uber.com/v1/endpoints/

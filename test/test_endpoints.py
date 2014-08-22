import unittest

from betamax import Betamax
from app import app

with Betamax.configure() as config:
    config.cassette_library_dir = 'test/fixtures'

test_auth_token = '42Kq726Vv6lzJ0TMhXWsgUulVjRsxh'


class TestCases(unittest.TestCase):
    def setUp(self):
        self.test_app = app.test_client()
        self.session = app.requests_session

    def test_health_endpoint(self):
        """Assert that the health endpoint works."""
        response = app.test_client().get('/health')
        self.assertEquals(response.data, ';-)')

    def test_root_endpoint(self):
        """Assert that the / endpoint correctly redirects to login.uber.com."""
        response = app.test_client().get('/')
        self.assertIn('login.uber.com', response.data)

    def test_products_endpoint_returns_success(self):
        """Assert that the products endpoint returns success.

        When a valid key is passed in.
        """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = test_auth_token
            with Betamax(app.requests_session).use_cassette('products_success'):
                response = client.get('/products')
        self.assertEquals(response.status_code, 200)

    def test_products_endpoint_returns_failure(self):
        """Assert that the products endpoint returns failure.

        When an invalid key is passed in.
        """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = 'NOT_A_CODE'
            with Betamax(self.session).use_cassette('products_failure'):
                response = client.get('/products')
        self.assertEquals(response.status_code, 401)

    def test_time_estimates_endpoint_returns_success(self):
        """Assert that the time estimates endpoint returns success.

        When a valid key is passed in.
        """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = test_auth_token
            with Betamax(app.requests_session).use_cassette('time_estimates_success'):
                response = client.get('/time')
        self.assertEquals(response.status_code, 200)

    def test_time_estimates_endpoint_returns_failure(self):
        """Assert that the time estimates endpoint returns failure.

        When an invalid key is passed in.
        """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = 'NOT_A_CODE'
            with Betamax(app.requests_session).use_cassette('time_estimates_failure'):
                response = client.get('/time')
        self.assertEquals(response.status_code, 401)

    def test_price_estimates_endpoint_returns_success(self):
        """Assert that the price estimates endpoint returns success.

        When a valid key is passed in.
        """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = test_auth_token
            with Betamax(app.requests_session).use_cassette('price_estimates_success'):
                response = client.get('/price')
        self.assertEquals(response.status_code, 200)

    def test_price_estimates_endpoint_returns_failure(self):
        """Assert that the price estimates endpoint returns failure.

        When an invalid key is passed in.
        """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = 'NOT_A_CODE'
            with Betamax(app.requests_session).use_cassette('price_estimates_failure'):
                response = client.get('/price')
        self.assertEquals(response.status_code, 401)

    def test_history_endpoint_returns_success(self):
        """Assert that the history endpoint returns success.

        When a valid key is passed in.
        """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = test_auth_token
            with Betamax(app.requests_session).use_cassette('history_success'):
                response = client.get('/history')
        self.assertEquals(response.status_code, 200)

    def test_history_endpoint_returns_failure(self):
        """Assert that the price estimates endpoint returns failure.

        When an invalid key is passed in.
        """
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = 'NOT_A_CODE'
            with Betamax(app.requests_session).use_cassette('history_failure'):
                response = client.get('/history')
        self.assertEquals(response.status_code, 401)

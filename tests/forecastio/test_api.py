import errno
import mock
import requests
import requests_mock
import socket
import time
import unittest
import urllib2

from appletea import forecastio
from appletea.forecastio.models import Forecast


def _urlq(items):
    l = []
    for k, v in items:
        l.append('%s=%s' % (k, v))
    return '&'.join(l)


class TestApi(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'https://api.forecast.io/forecast'
        self.apikey = '238ff8ab86e8245aa668b9d9cf8e8'
        self.latitude = 51.036391
        self.longitude = 3.699794

    @requests_mock.Mocker()
    def test_get_forecast_raises_client_error_404(self, mock):
        mock.get(requests_mock.ANY, status_code=404, json={})
        with self.assertRaises(requests.HTTPError) as e_cm:
            forecastio.get_forecast(self.apikey, self.latitude, self.longitude)

        self.assertEquals(e_cm.exception.response.status_code, 404)

    @requests_mock.Mocker()
    def test_get_forecast_raises_server_error_503(self, mock):
        mock.get(requests_mock.ANY, status_code=503, json={})
        with self.assertRaises(requests.HTTPError) as e_cm:
            forecastio.get_forecast(self.apikey, self.latitude, self.longitude)

        self.assertEquals(e_cm.exception.response.status_code, 503)

    @requests_mock.Mocker()
    def test_get_forecast_calls_correct_url(self, mock):
        mock.get(requests_mock.ANY, json={})
        forecastio.get_forecast(self.apikey, self.latitude, self.longitude)

        expected_url = '%s/%s/%s,%s' % (self.baseurl, self.apikey,
            self.latitude, self.longitude)
        url = '%s://%s%s' % (mock.last_request.scheme,
            mock.last_request.netloc, mock.last_request.path)
        self.assertEquals(url, expected_url)

    @requests_mock.Mocker()
    def test_get_forecast_calls_correct_url_with_argument(self, mock):
        mock.get(requests_mock.ANY, json={})
        kwargs = {'unit':'si'}
        forecastio.get_forecast(self.apikey, self.latitude, self.longitude, **kwargs)

        expected_url = '%s/%s/%s,%s?%s' % (self.baseurl, self.apikey,
            self.latitude, self.longitude, _urlq(kwargs.items()))
        url = '%s://%s%s?%s' % (mock.last_request.scheme,
            mock.last_request.netloc, mock.last_request.path,
            mock.last_request.query)
        self.assertEquals(url, expected_url)

    @requests_mock.Mocker()
    def test_get_forecast_calls_correct_url_with_multi_argument(self, mock):
        mock.get(requests_mock.ANY, json={})
        kwargs = {'unit':'si', 'lang':'en'}
        forecastio.get_forecast(self.apikey, self.latitude, self.longitude, **kwargs)

        expected_url = '%s/%s/%s,%s?%s' % (self.baseurl, self.apikey,
            self.latitude, self.longitude, _urlq(kwargs.items()))
        url = '%s://%s%s?%s' % (mock.last_request.scheme,
            mock.last_request.netloc, mock.last_request.path,
            mock.last_request.query)
        self.assertEquals(url, expected_url)

    @requests_mock.Mocker()
    def test_get_forecast_returns_object_model(self, mock):
        mock.get(requests_mock.ANY, json={})
        r = forecastio.get_forecast(self.apikey, self.latitude, self.longitude)

        self.assertIsInstance(r, Forecast)
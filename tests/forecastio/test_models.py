import json
import os.path as osp
import requests
import unittest

from appletea.forecastio.models import (
    Forecast, ForecastioDataPoint, ForecastioDataBlock)


class TestModels(unittest.TestCase):
    def setUp(self):
        response = requests.Response()
        json_file = osp.join(
            osp.dirname(osp.abspath(__file__)), 'data/test.json')
        with open(json_file) as fp:
            self.json_data = json.loads(fp.read())
        self.forecast = Forecast(self.json_data, response)

    def test_get_currently_forecast_returns_data_point_object(self):
        self.assertIsInstance(self.forecast.currently, ForecastioDataPoint)

    def test_get_minutely_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.minutely, ForecastioDataBlock)

    def test_get_hourly_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.hourly, ForecastioDataBlock)

    def test_get_daily_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.daily, ForecastioDataBlock)

    def test_get_alerts_forecast_returns_alert_object_list(self):
        self.assertIsInstance(self.forecast.alerts, list)

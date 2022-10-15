import os

import pandas as pd
import requests


class APIBMEHandler:

    def __init__(self):
        self.url_base = 'https://miax-gateway-jog4ew3z3q-ew.a.run.app'
        self.competi = 'mia_6'
        self.user_key = os.environ['MIAX_API_KEY']

    def get_ticker_master(self, market):
        url = f'{self.url_base}/data/ticker_master'
        params = {'competi': self.competi,
                  'market': market,
                  'key': self.user_key}
        response = requests.get(url, params)
        tk_master = response.json()
        maestro_df = pd.DataFrame(tk_master['master'])
        return maestro_df

    def get_close_data_ticker(self, market, ticker):
        url = f'{self.url_base}/data/time_series'
        params = {'market': market,
                  'key': self.user_key,
                  'ticker': ticker}
        response = requests.get(url, params)
        tk_data = response.json()
        series_data = pd.read_json(tk_data, typ='series')
        return series_data
    
    def get_ohlc_data_ticker(self, market, ticker):
        url = f'{self.url_base}/data/time_series'
        params = {'market': market,
                  'key': self.user_key,
                  'ticker': ticker,
                  'close': False}
        response = requests.get(url, params)
        tk_data = response.json()
        series_data = pd.read_json(tk_data)
        return series_data

import utils 


def test_get_data():
    api_handler = utils.APIBMEHandler()
    master = api_handler.get_ticker_master('IBEX')
    data_close = api_handler.get_ohlc_data_ticker('IBEX', 'SAN')
    print(data_close)

test_get_data()

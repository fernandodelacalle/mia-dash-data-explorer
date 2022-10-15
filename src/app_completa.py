import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import utils


app = dash.Dash(__name__)

api_handler = utils.APIBMEHandler()

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="👁", className="header-emoji"),
                html.H1(children="MIAX DATA EXPLORER", className="header-title"),
                html.P(
                    children="mIAx API", 
                    className="header-description",
                ),
            ],
        className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Index", className="menu-title"),
                        dcc.Dropdown(
                            id="menu-index",
                            options=[
                                {"label": 'IBEX', "value": 'IBEX'},
                                {"label": 'DAX', "value": 'DAX'},
                                {"label": 'EUROSTOXX', "value": 'EUROSTOXX'},
                            ],
                            value="IBEX",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="ticker", className="menu-title"),
                        dcc.Dropdown(
                            id="menu-ticker",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(children=[
                dcc.Graph(
                    id='example-graph',
                ),
            ],
            className="wrapper",
        )
    ])


@app.callback(
    Output('menu-ticker', 'options'),
    Input('menu-index', 'value'))
def update_ticker_options(market):
    master = api_handler.get_ticker_master(market)
    lista_tikers = list(master.ticker)
    options = [{'label': tck, 'value': tck} for tck in lista_tikers]
    return options

@app.callback(
    Output('menu-ticker', 'value'),
    Input('menu-ticker', 'options'))
def update_ticker_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('example-graph', 'figure'),
    Input('menu-ticker', 'value'),
    State('menu-index', 'value'))
def update_graph(ticker, market):
    data_to_plot = api_handler.get_ohlc_data_ticker(market, ticker)
    fig = go.Figure(
        go.Candlestick(
            x=data_to_plot.index,
            open=data_to_plot['open'],
            high=data_to_plot['high'],
            low=data_to_plot['low'],
            close=data_to_plot['close']
        )
    )
    return fig

if __name__ == '__main__':
    #app.run_server(host="0.0.0.0", debug=False, port=8080)
    app.run(debug=True)
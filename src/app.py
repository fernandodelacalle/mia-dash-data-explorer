import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd


import utils


app = dash.Dash(__name__)

ah = utils.APIBMEHandler()


app.layout = html.Div(
    children=[
        html.H1('MIAX Data EXPLORER'),
        html.P('mIAx API'),
        dcc.Dropdown(
            id='menu-index',
            options=[
                {'label': 'IBEX', 'value': 'IBEX'},
                {'label': 'DAX', 'value': 'DAX'},
                {'label': 'EUROSTOXX', 'value': 'EUROSTOXX'},
            ],
            value='IBEX'
        ),
        dcc.Dropdown(
            id='menu-ticker',
        ),
        dcc.Graph(
            id='example-graph',
        )
    ]
)



@app.callback(
    Output('menu-ticker', 'options'),
    Input('menu-index', 'value')
)
def change_ticker_menu_options(market):
    master = ah.get_ticker_master(market=market)
    ticker_options = [
        {'label': tck, 'value': tck} 
        for tck in master.ticker
    ]
    return ticker_options


@app.callback(
    Output('menu-ticker', 'value'),
    Input('menu-ticker', 'options'),
)
def select_tck(ticker_options):
    return ticker_options[0]['value']


@app.callback(
    Output('example-graph', 'figure'),
    State('menu-index', 'value'),
    Input('menu-ticker', 'value'),
)
def change_figure(market, tck):
    data = ah.get_close_data_ticker(market=market, ticker=tck)
    fig = px.line(data)
    return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False, port=8080)

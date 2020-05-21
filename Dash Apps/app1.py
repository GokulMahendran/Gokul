import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

confirmed_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
confirmed_df = confirmed_df.groupby("Country/Region").sum()
recoverd_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
recoverd_df = recoverd_df.groupby("Country/Region").sum()
death_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
death_df = death_df.groupby("Country/Region").sum()

country = confirmed_df.iloc[:, -1].sort_values(ascending=False)[:25].index


def fig_fun(df, Title):
    dates = [i[:-3] for i in df.columns[2:]]
    data = []
    for i in df.index:
        if i in country:
            val = df[df.index == i].iloc[0][2:]
            data.append(go.Scatter(x=dates,
                                   y=val,
                                   name=i,
                                   opacity=.9,
                                   mode="lines+markers",
                                   marker=dict(symbol="circle-open",
                                               size=3)))
        else:
            val = df[df.index == i].iloc[0][2:]
            data.append(go.Scatter(x=dates,
                                   y=val,
                                   name=i,
                                   visible="legendonly",
                                   opacity=.9,
                                   mode="lines+markers",
                                   marker=dict(symbol="circle-open",
                                               size=3)))
    layout = go.Layout(title=dict(text=Title,
                                  font=dict(color="white"),
                                  x=.45),
                       showlegend=True,
                       plot_bgcolor="Black",
                       paper_bgcolor="Black",
                       legend=dict(font=dict(color="white")),
                       xaxis=dict(title=dict(text="Date",
                                             font=dict(color="white")),
                                  tickfont=dict(color="white"),
                                  showgrid=False,
                                  ),
                       yaxis=dict(title=dict(text="No_of_" + Title,
                                             font=dict(color="white")),
                                  tickfont=dict(color="white"),
                                  showgrid=False))
    fig = go.Figure(data=data, layout=layout)
    return fig


confirmed_fig = fig_fun(confirmed_df, "Confirmed Cases")
recoverd_fig = fig_fun(recoverd_df, "Recoverd Cases")
death_fig = fig_fun(death_df, "Death Cases")
d = {"Confirmed Cases": confirmed_fig, "Recovered Cases": recoverd_fig, "Death Cases": death_fig}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID])
server=app.server
row1 = dbc.Row([
    dbc.Col([
        dcc.Dropdown(
            className="dropdown_styling",
            id="my_ticker_symbol",
            options=[{"label": "Confirmed Cases", "value": "Confirmed Cases"},
                     {"label": "Recovered Cases", "value": "Recovered Cases"},
                     {"label": "Death Cases", "value": "Death Cases"}
                     ],
            value="Confirmed Cases"
        ),
    ], width=11),
    dbc.Col([
        html.Button(className="btn btn-bubble", children='Submit', id='Submit-Button', n_clicks=0),
    ])
], no_gutters=True)

row2 = dbc.Row([
    dbc.Col([
        dcc.Graph(
            id="Lineplot",
            figure=confirmed_fig
        )
    ], width=12)
])

app.layout = html.Div([row1,
                       row2
                       ])


@app.callback(Output("Lineplot", "figure"),
              [Input("Submit-Button", "n_clicks")],
              [State("my_ticker_symbol", "value")])
def update_dist(n_clicks, variable):
    fig = d[variable]
    return fig


if __name__ == "__main__":
    app.run_server()
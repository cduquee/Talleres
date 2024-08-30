# -*- coding: utf-8 -*-

# Ejecute esta aplicación con 
# python app1.py
# y luego visite el sitio 
# http://127.0.0.1:8050/ 
# en su navegador.

import dash
from dash import dcc  # dash core components
from dash import html # dash html components
import plotly.express as px
import pandas as pd
from numpy import random as rm

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# en este primer ejemplo usamos unos datos de prueba que creamos directamente
# en un dataframe de pandas

rm.seed(seed=1)

df = pd.DataFrame({
    "Trimestre": ["Q1", "Q2", "Q3", "Q4", "Q1", "Q2", "Q3", "Q4"],
    "Ventas (und)": [round(rm.normal(250,20)), round(rm.normal(400,10)), round(rm.normal(700,100)), round(rm.normal(1500,200)), 
              round(rm.normal(100,5)), round(rm.normal(200,20)), round(rm.normal(300,50)), round(rm.normal(500,10))],
    "Producto": ["Manzana", "Manzana", "Manzana", "Manzana", "Mandarina", "Mandarina", "Mandarina", "Mandarina"]
})

fig = px.bar(df, x="Trimestre", y="Ventas (und)", color="Producto", barmode="group", color_discrete_map={
        'Manzana': '#fe2e2e',
        'Mandarina': '#fb8b24'
    })

app.layout = html.Div(children=[
    html.H1(children='Tablero de Ventas'),

    html.Div(children='''
        Histograma de ventas de manzana y mandarina por trimestre
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.Div(children='''
        En este gráfico se observa el número de de unidades vendidas de manzanas y mandarina por trimestre.
    '''),
    html.Div(
        className="Columnas",
        children=[
            html.Ul(id='my-list', children=[html.Li(i) for i in df.columns])
        ],
    )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

#python .\Taller4_AWS\base\app1.py
#.\venv.AC\Scripts\activate
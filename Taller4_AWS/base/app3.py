import dash
from dash import dcc  # dash core components 
from dash import html # dash html components
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
print(df.columns)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1("Dashboard: GDP per capita/Life Expentancy for continents", style={"text-align":"center", "font-weight":"bold","font-size":30}),
    html.Div([dcc.Graph(id='graph-with-slider')]),
    html.Div([dcc.Graph(id='graph-asia-with-slider2')],style={'display': 'inline-block', 'width': '49%'}),
    html.Div([dcc.Graph(id='graph-america-with-slider2')],style={'display': 'inline-block', 'width': '49%'}),
    html.Div([dcc.Graph(id='graph-europe-with-slider2')],style={'display': 'inline-block', 'width': '49%'}),
    html.Div([dcc.Graph(id='graph-africa-with-slider2')],style={'display': 'inline-block', 'width': '49%'}),

    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


@app.callback(
    [Output('graph-with-slider', 'figure'), 
     Output('graph-asia-with-slider2', 'figure'),
     Output('graph-america-with-slider2', 'figure'),
     Output('graph-europe-with-slider2', 'figure'),
     Output('graph-africa-with-slider2', 'figure')],
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    
    fig1 = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
                     size="pop", color="continent", hover_name="country", 
                     log_x=True, size_max=55,
                     labels={
                     "pop": "Population",
                     "gdpPercap": "GDP per cápita",
                     "lifeExp": "Life Expectancy",
                     "continent": "Continent"
                     },
                     title="Life expectancy vs. GDP per cápita across the years")
    
    fig_asia = px.pie(data_frame=filtered_df[filtered_df["continent"]=="Asia"].sort_values("gdpPercap").tail(5), names="country", values="gdpPercap", color="country", title="Top 5 countries GDP per capita (Asia)")
    fig_ame = px.pie(data_frame=filtered_df[filtered_df["continent"]=="Americas"].sort_values("gdpPercap").tail(5), names="country", values="gdpPercap", color="country", title="Top 5 countries GDP per capita (Americas)")
    fig_eu = px.pie(data_frame=filtered_df[filtered_df["continent"]=="Europe"].sort_values("gdpPercap").tail(5), names="country", values="gdpPercap", color="country", title="Top 5 countries GDP per capita (Europe)")
    fig_afr = px.pie(data_frame=filtered_df[filtered_df["continent"]=="Africa"].sort_values("gdpPercap").tail(5), names="country", values="gdpPercap", color="country", title="Top 5 countries GDP per capita (Africa)")
    fig1.update_layout(transition_duration=500)
    fig_asia.update_layout(transition_duration=500)
    fig_ame.update_layout(transition_duration=500)
    fig_eu.update_layout(transition_duration=500)
    fig_afr.update_layout(transition_duration=500)

    return fig1, fig_asia, fig_ame, fig_eu, fig_afr


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)

#python .\Taller4_AWS\base\app3.py
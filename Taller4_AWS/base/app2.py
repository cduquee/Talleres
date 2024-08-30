import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
    html.H6("Modifique el valor en la caja de texto para ver el funcionamiento de los callbacks"),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='Ingresa tu nombre', type='text')]),
    html.Br(),
    html.Div(id='my-output'),
    ]
)


@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    if input_value == "Ingresa tu nombre" or input_value == "":
        output = ""
    else:
        output = 'Output: {}'.format(f'Hola, {input_value}')
    return output


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

#python .\Taller4_AWS\base\app2.py
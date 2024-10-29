import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
import psycopg2
from dotenv import load_dotenv # pip install python-dotenv
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

dir_actual = os.path.dirname(__file__)
env_path = os.path.join(dir_actual, 'env','app-sofia.env')

# load env 
load_dotenv(dotenv_path=env_path)
# extract env variables
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
DBNAME=os.getenv('DBNAME')

#connect to DB
print(DBNAME)
print(USER)
print(PASSWORD)
print(HOST)
print(PORT)
engine = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

cursor = engine.cursor()

query = """
select distinct team
from prodq1
order by team asc;"""
cursor.execute(query)
result = cursor.fetchall()

query2 = """
select distinct department
from prodq1
order by department asc;"""
cursor.execute(query2)
result2 = cursor.fetchall()

query3 = """
select distinct quarter
from prodq1
order by quarter asc;"""
cursor.execute(query3)
result3 = cursor.fetchall()


print(result3)

app.layout = html.Div(
    [
    html.H1("Dashboard Manufactura", style={'color': '#2ff21d', 'fontSize': 40, 'font-weight': 'bold', 'text-align':'center'}),
    html.H6("Seleccione Información a Consultar", style={'font-weight': 'bold'}),
    html.Div(["Day: ",
              dcc.Dropdown(id='day', value='Monday', 
                           options=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'])]),
    html.Div(["Quarter: ",
              dcc.Dropdown(id='quarter', value='Quarter1', 
                           options=[result3[i][0] for i in range(0,len(result3))])]),
    html.Div(["Team: ",
              dcc.Dropdown(id='team', value=1, 
                           options= [result[i][0] for i in range(0,12)])]),
    html.Div(["Department: ",
              dcc.Dropdown(id='department', value='sweing', 
                           options=[result2[i][0] for i in range(0,len(result3))])]),
    html.Br(),
    html.Br(),
    html.H6("Estadísticas:",style={'font-weight': 'bold'}),
    html.Br(),
    html.Div(["Targeted Productivity:", html.Div(id='output-target')]),
    html.Div(["Actual Productisvity:", html.Div(id='output-actual')]),
    ]
)


@app.callback(
    Output(component_id='output-target', component_property='children'),
    Output(component_id='output-actual', component_property='children'),
    Input(component_id='day', component_property='value'),
    Input(component_id='quarter', component_property='value'),
    Input(component_id='department', component_property='value'),
    Input(component_id='team', component_property='value')


)
def update_output_div(day, quarter, department, team):
    
    cursor = engine.cursor()
    query = f"""
    select targeted_productivity
    from prodq1
    where day='{day}' AND quarter='{quarter}' AND department='{department}' AND team='{team}';"""
    cursor.execute(query)
    result = cursor.fetchall()
    try:
        value1 = result[0][0]
        print(value1)
    except IndexError:
        value1 = "dato no existe!"

    cursor = engine.cursor()
    query = f"""
    select actual_productivity
    from prodq1
    where day='{day}' AND quarter='{quarter}' AND department='{department}' AND team='{team}';"""
    cursor.execute(query)
    result = cursor.fetchall()
    try:
        value2 = result[0][0]
        print(value2)
    except IndexError:
        value2 = "dato no existe!"

    return '{:.2f}'.format(value1) if isinstance(value1, float) else value1, '{:.2f}'.format(value2) if isinstance(value2, float) else value2
        

if __name__ == '__main__':
    app.run_server(debug=True, port=8040)
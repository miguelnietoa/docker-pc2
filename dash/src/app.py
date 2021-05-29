# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pandas.io.sql as psql
import psycopg2
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#establishing the connection
conn = psycopg2.connect(
   database='indian_prison_db', user='postgres', password='sa123456', host='postgresdb', port='5432'
)
df = psql.read_sql('SELECT * FROM indian_prison', conn, index_col='id')
conn.close()

app.layout = html.Div([
    html.H1('Hi')

])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd
import pandas.io.sql as psql
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#establishing the connection
db_started = False
while (not db_started):
    try: 
        conn = psycopg2.connect(
            database='indian_prison_db',
            user='postgres', password='sa123456',
            host='postgresdb', port='5432'
        )
        db_started = True
    except:
        pass
    
df = psql.read_sql('SELECT * FROM indian_prison', conn, index_col='id')
conn.close()

app.layout = html.Div([
    html.H2('Chart1'),
    html.Div([
        dcc.Graph(id='chart1'),
        dcc.Markdown('''La mayoría de personas en prisión son del sexo másculino. Además, se puede visualizar la gran diferencia existente si se ven los casos de *Bajo juicio* y *Convictos* frente a *Detenidos* y *Otras razones*, teniendo los primeros una cantidad superior. Cabe resaltar que la mayoría de personas están bajo juicio, lo que puede dar posibilidad a que la cantidad de personas en prisión reduzcan dependiendo del resultado del juicio.

**NOTA**: Tener en cuenta que los valores del eje *y* están a una escala de *1M = 10^6*.'''),
    ]),

    html.H2('Chart2'),
    html.Div([
        dcc.Graph(id='chart2'),
        dcc.Markdown('''La cantidad de personas detenidas (*total_detenues*) en prisión ha mantenido un comportamiento constante a lo largo de los años mostrados [2001-2013], mientras que la cantidad de personas bajo juicio (*total_under_trial*) no siempre aumentan o disminuyen, es decir, su comportamiento es inestable, sin embargo, la tendencia general es ascendente pasando de tener aprox. 441634 personas en 2001 a 557000 en el año 2013. Por otro lado, la cantidad de personas que se encuentran en la carcel bajo otras razones (*total_others*) ha estado disminuyendo paulatinamente.'''),
    ]),

    html.H2('Chart3'),
    html.Div([
        dcc.Graph(id='chart3'),
        dcc.Markdown('''La tendencia general de la cantidad de personas en prisión es ascendente, aunque se puede notar que en el periodo del 2008 al 2010 se redujo el número de prisioneros en India. Otra información importante es que la mayor cantidad de esta población se ubica en el estado llamado **Uttar Pradesh**.'''),
    ]),
    html.H2('Chart4'),
    html.Div([
        dcc.Graph(id='chart4'),
        dcc.Markdown('''Gracias a este gráfico es posible observar que la mayoría de personas en prisión están en los tipos de insticiones "Central Jail" y "District Jail". La diferencia que tienen estos dos contra el resto es bastante amplia.''')
    ]),
])

@app.callback(
    Output('chart1', 'figure'),
    Input('chart1', 'id')
)
def create_chart1(id):
    x = ['Convictos', 'Bajo juicio', 'Detenidos', 'Otras razones']
    male = [df['male_convicts'].sum(),
        df['male_under_trial'].sum(),
        df['male_detenues'].sum(),
        df['male_others'].sum()]

    female = [df['female_convicts'].sum(),
            df['female_under_trial'].sum(),
            df['female_detenues'].sum(), 
            df['female_others'].sum()]

    df_ = pd.DataFrame({'Másculino': male, 'Femenino': female})
    return px.bar(df_, x=x, y=['Másculino', 'Femenino'], barmode='group', labels={'variable': 'Sexo'})

@app.callback(
    Output('chart2', 'figure'),
    Input('chart2', 'id')
)
def create_chart2(id):
    casesbyyear = df.groupby('year').sum().reset_index()
    fig = go.Figure()
    toplot = ['total_convicts', 'total_under_trial', 'total_detenues', 'total_others']

    for col in toplot:
        fig.add_trace(go.Scatter(x=casesbyyear['year'],
                            y=casesbyyear[col],
                            mode='lines+markers',
                                name=col))
    return fig



@app.callback(
    Output('chart3', 'figure'),
    Input('chart3', 'id')
)
def create_chart3(id):
    totalbyyear = df.groupby(['year', 'state_ut_name']).sum().reset_index()
    return px.bar(totalbyyear, x='year', y='grand_total', color='state_ut_name', barmode='stack', title='Personas en prisión por año')

@app.callback(
    Output('chart4', 'figure'),
    Input('chart4', 'id')
)
def create_chart4(id):
    totalbyjail_type = df[df.jail_type != 'Total'].groupby('jail_type')['grand_total'].sum().reset_index()
    return px.pie(totalbyjail_type, values='grand_total', names='jail_type', title='Número de prisoneros por tipo de institución')


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
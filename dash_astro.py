import pandas as pd
from jupyter_dash import JupyterDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from collections import deque
from datetime import datetime
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

app=JupyterDash(__name__)

#importation données astronautes
df_astro = pd.read_csv('astronauts.txt', sep=',')
df_unique_astro = df_astro.drop_duplicates(subset ="name", keep = 'first')

listOrigin = df_unique_astro['nationality'].unique().tolist()

colors = {
    'background': '#2d1636',
    'text': '#ffffff'
}

fig = px.bar(df_unique_astro, x='name', y='total_hrs_sum')

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig2 = px.scatter(
        df_astro, x="year_of_mission", y='total_hrs_sum', 
        color="nationality", size='total_hrs_sum', 
        hover_data=['name'],
        labels={'year_of_mission':'Année de la mission',
                   'total_hrs_sum':"Nombre d'heures en mission"})


fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

app.layout= html.Div(
    style={'backgroundColor': colors['background']}, 
    children = [
        html.P(
            html.Img(src='https://zupimages.net/up/21/19/15w1.png', style={'marginTop':20}),
            style={'text-align':'center'}),
        html.H2("Les missions spatiales par pays et par année:", style ={'font':'Calibri', 'color': colors['text'], 'font-family': 'Calibri', 'marginLeft':20}),
        html.P(html.Iframe(src='https://flo.uri.sh/visualisation/6115650/embed', width=1500, height=900),style={'text-align':'center'}),
        html.P(
        html.Img(src='https://zupimages.net/up/21/19/q0s2.png', style={'marginTop':20}),
           style={'text-align':'center'}),
        html.H2("Quel est le premier citoyen de chaque pays à âtre aller dans l'espace ?", style ={'font':'Calibri', 'color': colors['text'], 'font-family': 'Calibri', 'marginLeft':20}),
        html.P(html.Iframe(src='https://flo.uri.sh/visualisation/6118562/embed', width=1500, height=600),style={'text-align':'center'}),
        dbc.Row([
            dbc.Col(
                #html.Img(src='https://zupimages.net/up/21/19/4z1f.png'),
                    ),
            dbc.Col(html.Div([
                html.H2("Sélectionnez un pays:", style ={'font':'Calibri', 'color': colors['text'], 'font-family': 'Calibri', 'marginLeft':20}),
                dcc.Dropdown(
                        id='country',
                        options=[{'label': i, 'value': i} for i in listOrigin],
                        value='U.S.',
                        style = {'marginRight': 1600, 'marginLeft':10}
                    ),
                html.H2("Temps passés dans l'espace pour les astronautes de ce pays:", style ={'font':'Calibri', 'color': colors['text'], 'font-family': 'Calibri', 'marginLeft':20})
            ]))]),
        dcc.Graph(
            id='graph',
            figure=fig
        ),
        html.P(
            html.Img(src='https://zupimages.net/up/21/19/ydfn.png', style={'marginTop':20}),
           style={'text-align':'center'}),
        html.H2("Heures passés dans l'espace par mission, pour ce pays:", style ={'font':'Calibri', 'color': colors['text'], 'font-family': 'Calibri', 'marginLeft':20}),
        dcc.Graph(id="scatter_plot", 
            figure = fig2 ),
    
])

@app.callback([Output(component_id='graph', component_property='figure'),
              Output(component_id='scatter_plot', component_property='figure')],
             Input(component_id='country',component_property='value'))

def update_graph(country):
    #fig
    mask = df_unique_astro['nationality']==country
    fig = px.bar(df_unique_astro[mask], x='name', y='total_hrs_sum', labels={'name':'','total_hrs_sum':"Nombre d'heures en mission"})
    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])
    #fig2
    fig2 = px.scatter(
        df_unique_astro[mask], x="year_of_mission", y='total_hrs_sum', 
        color="nationality", size='total_hrs_sum', 
        hover_data=['name'],
        labels={'year_of_mission':'Année de la mission',
                   'total_hrs_sum':"Nombre d'heures en mission"})
    fig2.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])
    return fig, fig2

app.run_server(mode='external', port=8000)

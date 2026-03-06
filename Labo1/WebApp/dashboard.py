import dash
from dash import dcc, html, Input, Output, ctx, dash_table, State
import plotly.express as px
import pandas as pd
import requests
import dto.DTOs
import APIClient as ap
from dataclasses import asdict

client = ap.APIClient("http://127.0.0.1:8000")

app = dash.Dash(__name__)

def get_year():
    return client.getAvgRatingByYear()    

app.layout = html.Div(children=[
    
    dcc.Interval(
        id='chronometre-api',
        interval=5000, 
        n_intervals=0
    ),

    html.Div(
        id='label-total-movies',
        children="Films au total : Chargement...",
        style={
            'position': 'absolute',
            'top': '20px',
            'right': '20px',
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'padding': '10px 15px',
            'borderRadius': '5px',
            'fontWeight': 'bold',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'
        }
    ),
    
    html.H1(children='Labo 1 : WebMinning IMDB movies', style={'textAlign': 'center'}),

    html.Div([
        dcc.Input(
            id='input-search', 
            type='text', 
            placeholder='Titre ou mots-clés...',
            style={'marginRight': '10px', 'width': '300px'}
        ),
        
        html.Button(
            'Rechercher', 
            id='btn-search', 
            n_clicks=0, 
            style={'cursor': 'pointer'}
        )
    ], style={'padding': '20px', 'textAlign': 'center'}),
    html.Div(
        id='container-table', 
        style={'display': 'none', 'marginBottom': '20px'},
        children=[
        dash_table.DataTable(
            id='table-movies-search',
            columns=[
                {"name": "Rang", "id": "rank"},
                {"name": "Titre", "id": "title"},
                {"name": "Année", "id": "year"},
                {"name": "Durée", "id": "duration"},
                {"name": "Note", "id": "rating"},
                {"name": "Votes", "id": "votes"},
                {"name": "Score", "id": "score"},
            ],
            data=[],
            
            style_table={'overflowX': 'auto', 'width': '80%', 'margin': 'auto', 'marginBottom': '20px'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#f4f4f4', 'fontWeight': 'bold'},
            page_size=10,        
            sort_action="native" 
        )]
    ), 


    html.Div(children='Sélectionnez une année pour voir les meilleurs films de cette année :', 
             style={'marginBottom': '20px', 'textAlign': 'center'}),

    html.Div(children=dcc.Dropdown(
        id='dropdown-year',
        options=[{'label': f"{year.year} : {year.doc_count}", 'value': year.year} for year in get_year()],
        value=1994, 
        clearable=False,
        style={
            'width': '50%', 
            'margin': 'auto',     
            'textAlign': 'center' 
        }
    ), style={'marginBottom': '20px'}),
    dash_table.DataTable(
        id='table-hits',
        columns=[
            {"name": "Rang", "id": "rank"},
            {"name": "Titre", "id": "title"},
            {"name": "Année", "id": "year"},
            {"name": "Durée", "id": "duration"},
            {"name": "Note", "id": "rating"},
            {"name": "Votes", "id": "votes"}
        ],
        data=[],
        style_table={'overflowX': 'auto', 'width': '80%', 'margin': 'auto', 'margin-top': '20px'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#f4f4f4', 'fontWeight': 'bold'},
        page_size=10,        
        sort_action="native" 
    ),
    html.Div([
        dcc.Graph(id='graph-evolution-temporelle')
    ], style={'padding': '20px'})
])

@app.callback(
    Output('label-total-movies', 'children'),
    Input('chronometre-api', 'n_intervals')
)
def update_cpt_movies(n_tics):
    try:
        resultat_dto = client.getCountNbMovies()
        total = resultat_dto.value
        return f"Films au total : {total}"
        
    except Exception as e:
        print(f"Erreur compteur : {e}")
        return "Films au total : Hors ligne"


@app.callback(
    [Output('table-movies-search', 'data'),
     Output('container-table', 'style')],    
    Input('btn-search', 'n_clicks'), 
    State('input-search', 'value')      
)
def update_table_search(n_clicks, mots_cles):    
    if n_clicks == 0 or not mots_cles:
        return [], {'display': 'none'}

    try:
        resultats_dto = client.searchByKeyword(mots_cles)
        if not resultats_dto:
            return [], {'display': 'none'}
        datas = []
        for resultat in resultats_dto:
            movie_dict = asdict(resultat.movie)
            movie_dict['score'] = resultat.score
            datas.append(movie_dict)

        return datas, {'display': 'block', 'marginTop': '20px'}
            
    except Exception as e:
        print(f"Erreur API : {e}")
        return []

@app.callback(
    Output('graph-evolution-temporelle', 'figure'),
    Input('chronometre-api', 'n_intervals')
)
def update_graph_historique(n):
    try:
        results_dto = client.getAvgRatingByYear()        
        df = pd.DataFrame([asdict(res) for res in results_dto])
        df = df.sort_values('year')
        fig = px.line(
            df, 
            x='year', 
            y='avg',
            title="Évolution de la note moyenne des films par année",
            labels={'year': 'Année', 'avg': 'Note Moyenne (IMDb)'},
            markers=True 
        )
        fig.update_layout(
            clickmode='event+select',
            hovermode="x unified",
            template="plotly_white",
            yaxis_range=[0, 10] 
        )
        return fig

    except Exception as e:
        print(f"Erreur Graphique : {e}")
        return px.scatter(title="Erreur de chargement des données")

@app.callback(
    [Output('table-hits', 'data'),
     Output('dropdown-year', 'value')], 
    [Input('dropdown-year', 'value'),
     Input('graph-evolution-temporelle', 'clickData')]
)
def update_based_on_click(dropdown_year, click_data):
    trigger = ctx.triggered_id
    
    year = dropdown_year 
    if trigger == 'graph-evolution-temporelle' and click_data:
        year = click_data['points'][0]['x']

    print(year)
    try:
        res = client.getTopMovieByYear(year)
        return [asdict(f) for f in res], year
    except:
        return [], year


if __name__ == '__main__':
    app.run(debug=True)
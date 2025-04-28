import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd





burger_component = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        dmc.Burger(
            id="burger-button",
            opened=True,
            style={"marginLeft": "80px"},
            color='#587362'
        )
    ]
)

card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="dash/assets/person.png",  # J'ai ajouté le slash au début
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4 py-2",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                        html.H6("Nom:", className="card-subtitle mb-2 text-muted"),
                        html.H6("Département:", className="card-subtitle mb-2 text-muted"),
                           
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    style={
        'backgroundColor': 'white',
        'height': '115px',
        'width': '100%',
        'borderRadius': '15px',
        'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)',
        'overflow': 'hidden'  # Ajouté pour éviter que le contenu ne déborde
    },
)

def create_gauge_chart(value):
    # Gérer les valeurs NaN
    if pd.isna(value) or value is None:
        # Option 1: Afficher 0 comme valeur par défaut
        value = 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        # title={'text': title_text, 'font': {'size': 24}},
        delta={'reference': 5, 'increasing': {'color': "#285939"}},
        gauge={
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "green"},
            'bar': {'color': "#285939", 'thickness': 1},
            'bgcolor': "white",
            'borderwidth': 2,
            'threshold': {
                'line': {'color': "#8C1F1F", 'width': 4},
                'thickness': 0.75,
                'value': 5}}))
    
    fig.update_layout(
        paper_bgcolor="white",
        font={
        'color': "#285939", 
        'family': "Arial"
    },
        autosize=True,
        margin=dict(l=15, r=15, t=15, b=20),
        
    )
    return fig

def create_gauge_task(value1):
    fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=value1,
    domain={'x': [0, 1], 'y': [0, 1]},
    number={'suffix': " %"},  # ✅ ici on ajoute le pourcentage
    delta={'reference': 50, 'increasing': {'color': "#285939"}},
    gauge={
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "green"},
        'bar': {'color': "#285939", 'thickness': 1},
        'bgcolor': "white",
        'borderwidth': 2,
        'threshold': {
            'line': {'color': "#8C1F1F", 'width': 4},
            'thickness': 0.75,
            'value': 50
        }
    }
))
    fig.update_layout(
        paper_bgcolor="white",
        font={
        'color': "#285939", 
        'family': "Arial"
    },
        autosize=True,
        margin=dict(l=15, r=15, t=15, b=20),
        
    )
    return fig




def create_pie_status(data, values, names,color_discrete_map):
    fig1 = px.pie(data, values=values, names=names,color=names,color_discrete_map=color_discrete_map, hole=.3)
    fig1.update_layout(
    title_font=dict(size=15, color='black', family='Arial'),
    autosize=True,
    margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig1

def create_bar_chart(data, x , y ):
    fig2 = px.bar(data, x=x, y=y,color_discrete_sequence=['#8C1F1F'],text=y)
    fig2.update_layout(
    autosize=True,
    xaxis_title="",
    yaxis_title="",
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="white",  # Supprime le fond général
    plot_bgcolor="white",
    yaxis=dict(
            showticklabels=False,  # Masque les valeurs de l’axe Y
            showgrid=False         # Optionnel : enlève les lignes horizontales
        )
    )
    fig2.update_traces(
        textposition='outside'  # Place le texte au-dessus des barres
    )
    return fig2



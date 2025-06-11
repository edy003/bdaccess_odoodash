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
        ),
    xaxis=dict(
            tickfont=dict(
                color="#8C1F1F",      # Couleur des ticks de l'axe X
                size=14,              # Taille du texte
                family="Arial Black",       # Optionnel : police propre
            )
        ),
    
    )
    fig2.update_traces(
        textposition='outside',# Place le texte au-dessus des barres
         textfont=dict(
            color="#8C1F1F",         # Couleur du texte au-dessus des barres
            # # size=14,                 # Taille du texte
            # family="",          # Police (même pour tout rendre harmonieux)
        ),
        
    )
    return fig2

def create_dropdown(label, options, dropdown_id, placeholder='Sélectionner...'):
    return html.Div([
        html.Div(label, style={
            'color': 'white',
            'fontSize': '14px',
            'fontWeight': 500,
            'lineHeight': '1.55',
        }),
        dcc.Dropdown(
            options=[{'label': str(option), 'value': option} for option in options],
            id=dropdown_id,
            placeholder=placeholder,
            style={'color': 'black'}
        )
    ])





def generate_chip_selector(
    id, 
    label, 
    options, 
    multiple=True, 
    color="blue", 
    value_default=[]
):
    """
    Génère un composant MantineProvider avec un ChipGroup personnalisé.

    Args:
        id (str): ID du ChipGroup.
        label (str): Titre affiché au-dessus du ChipGroup.
        options (list): Liste des options (valeurs et labels des chips).
        multiple (bool): Si True, permet la sélection multiple. Sinon, sélection unique.
        color (str): Couleur des chips (par défaut: "blue").
        value_default (list): Liste des valeurs sélectionnées par défaut.

    Returns:
        dmc.MantineProvider: Composant prêt à l'emploi.
    """

    return dmc.MantineProvider(
        theme={
            "components": {
                "Chip": {
                    "styles": {
                        "label": {
                            "width": "100%",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "padding": "8px 12px",
                        },
                        "input": {
                            ":checked + label": {
                                "backgroundColor": "#228BE6 !important",
                                "color": "white !important",
                            }
                        },
                        "checkIcon": {
                            "display": "none",
                        },
                    }
                }
            }
        },
        children=[
            html.Div(
                label, 
                style={
                    'color': 'white',
                    "fontSize": "14px",
                    "fontWeight": 500,
                    "lineHeight": "1.55",
                }
            ),
            html.Div(
                dmc.ChipGroup(
                    id=id,
                    multiple=multiple,
                    value=value_default,
                    children=[
                        dmc.Chip(
                            option,
                            value=option,
                            variant="filled",
                            color=color,
                            radius="md",
                            size="sm",
                            className="custom-chip"
                        )
                        for option in options
                    ],
                ),
                style={
                    "width": "100%",
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "10px",
                },
            ),
        ],
    )


import dash_mantine_components as dmc
from dash import html

def get_date_range_component(date_min, date_max, id="id"):
    return dmc.MantineProvider(
        theme={
            "colorScheme": "light",
            "primaryColor": "mygreen",
            "colors": {
                "mygreen": [
                    "#e6f0eb", "#cce0d6", "#99c1ad", "#66a384",
                    "#33845b", "#285939", "#1f452d", "#163021",
                    "#0d1c14", "#050d09"
                ]
            },
            "components": {
                "DatePickerInput": {
                    "styles": {
                        "dropdown": {"zIndex": '9999'},
                        "input": {"zIndex": '9999'},
                        "label": {"color": "white"}
                    }
                }
            }
        },
        children=html.Div(
            [
                dmc.DatePickerInput(
                    id=id,  # 👈 Id dynamique passé en paramètre
                    label="Date Range",
                    minDate=date_min,
                    maxDate=date_max,
                    type="range",
                    value=[date_min, date_max],
                    valueFormat="YYYY-MM-DD",
                    maw=300,
                ),
            ]
        )
    )


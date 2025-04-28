from dash import Dash, html,dcc,Input, Output,dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash
import pandas as pd
from widget import card
from app import employee_valid_rating
from datetime import datetime, timedelta, date



dash.register_page(__name__,order=2)

option_department = employee_valid_rating['department_id'].unique()

dropdown_employee=  html.Div([
        "employee",
        dcc.Dropdown(employee_valid_rating['name_x'].unique(), id='dropdown_employee')
    ])

cols_to_convert = ['start_date', 'expected_end_date', 'end_date', 'evaluation_date']
for col in cols_to_convert:
    employee_valid_rating.loc[:, col] = pd.to_datetime(employee_valid_rating[col], errors='coerce')
employee_valid_rating = employee_valid_rating[employee_valid_rating['start_date'].notna()]
date_min = employee_valid_rating['start_date'].min()
date_max = employee_valid_rating['start_date'].max()

date_range= dmc.MantineProvider(
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
                    "input": {"zIndex": '9999'}
                }
            }
        }
    },
    children=html.Div(
        [
            dmc.DatePickerInput(
                id="date-input",
                label="Date Range",
                description="Select a date range",
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





department = dmc.MantineProvider(
    theme={"components": {
        "Chip": {
            "styles": {
                "label": {
                    "width": "100%",  # Prend toute la largeur disponible
                    "justifyContent": "center",
                    "alignItems": "center",  
                    "padding": "8px 12px"  # Padding supplémentaire pour l'esthétique
                },
                "input": {
                        ":checked + label": {  # Ciblage du label lorsque l'input est coché
                            "backgroundColor": "#228BE6 !important",
                            "color": "white !important"
                        }
                    },
                "checkIcon": {
                    "display": "none"  # Cache l'icône de coche
                }
            }
        }
    }},
    children=[
        html.Div("Department"),
        # Conteneur pour gérer l'affichage vertical
        html.Div(
            dmc.ChipGroup(
                id="department1",
                multiple=True,
                value=[],
                children=[
                    dmc.Chip(
                        department,
                        value=department,
                        variant="filled",
                        color="blue",
                        radius="md",
                        size="sm",
                        className="custom-chip"
                    )
                    for department in option_department
                ]
            ),
            style={
                "width": "100%", 
                "display": "flex",
                "flexDirection": "column",  # Affichage en colonne
                "gap": "10px"  # Espacement entre les boutons
            }
        )
    ]
)


# Layout obligatoire
layout = html.Div(children=[
        # dcc.Store(id='sidebar-state', data=True),
        dbc.Row([
            dbc.Col(dbc.Row(dbc.Col(html.Div([
            dbc.Stack(
            [
                html.Div(date_range),
                html.Div(department),
                html.Div(dropdown_employee),
            ],
            gap=3,
        ),
            ])),),id='sidebar',width=2,
                    style={'backgroundColor': '#587362','height': '100vh','zIndex': '300','position':'fixed','left':'0','width': '16.666667%','top':'60px'}),
        dbc.Col(id='spacer-col',width=2,style={'backgroundColor': '#F2F2F2','marginTop':'60px'}),
        dbc.Col(html.Div([
        dbc.Row([
        dbc.Col(card,width=4),
        dbc.Col(html.Div(dbc.Card(
        dbc.CardBody(
        [
        html.H3("Projets Affectes", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
        html.H1(id='nbre_projet',className="text-center",style={'color':'#8C1F1F'}),
        ],style={
        'padding-top': '5px',  # Réduit l'espace en haut
        'padding-bottom': '0px',    
            }
        ,className="w-100")
        ,className="w-100 h-100 border-0")),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},className='ms-3 me-3'),
        dbc.Col(html.Div(dbc.Card(
        dbc.CardBody(
        [
        html.H3("Taches assignees", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
        html.H1(id='nbre_tache',className="text-center",style={'color':'#8C1F1F'}),
        ],style={
        'padding-top': '5px',  # Réduit l'espace en haut
        'padding-bottom': '0px',    
        }
        ,className="w-100")
        ,className="w-100 h-100 border-0")),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},className='me-3'),
        dbc.Col(html.Div(dbc.Card(
        dbc.CardBody(
        [
        html.H3("Delai moyen", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
        html.Div(id='date_delai',className="text-center",),
        ],style={
        'padding-top': '5px',  # Réduit l'espace en haut
        'padding-bottom': '0px',    
        }
        ,className="w-100")
        ,className="w-100 h-100 border-0")),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
        ],style={}, className=''),
        html.Div(dbc.Row([
        dbc.Col(html.Div(dbc.Card(
             [
             dbc.CardHeader(
            "Note moyenne",
            style={"padding": "5px", "fontSize": "14px", "height": "30px"}  # Ajuste ici selon besoin
            ),
            dbc.CardBody(
            dcc.Graph(id='taux_satisfaction',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False})
            ,style={"width": "100%", "height": "calc(100% - 30px)"}
           )
           ],style={"height": "100%",'width':'100%'}
           ),style={'height':'250px','backgroundColor':'white','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),width=6,className='me-3'),
        dbc.Col(html.Div(dbc.Card(
             [
             dbc.CardHeader(
            "Tache completes",
            style={"padding": "5px", "fontSize": "14px", "height": "30px"}  # Ajuste ici selon besoin
            ),
            dbc.CardBody(
            dcc.Graph(id='taux_task',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False}),
            style={"width": "100%", "height": "calc(100% - 30px)"}
           )
           ],style={"height": "100%",'width':'100%'}
           ),style={'height':'250px','backgroundColor':'white','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),width=True),
        ],className='mt-3 ',style={'overflowX':'hidden'})),

    html.Div(dbc.Row(dbc.Col(
    html.Div(dbc.Card(
        [
            dbc.CardHeader(
                "Note moyenne",
                style={"padding": "5px", "fontSize": "14px", "height": "30px"}
            ),
            dbc.CardBody(
                dash_table.DataTable(
                    id='datatable',
                    columns=[
                        {'name': 'employee', 'id': 'employee'},
                        {'name': 'tache', 'id': 'tache'},
                        {'name': 'manager', 'id': 'manager'},
                        {'name': 'statut', 'id': 'statut'},
                        {'name': 'progress', 'id': 'progression'},
                        {'name': 'note', 'id': 'note'},
                        {'name': 'comments', 'id': 'comments'},
                    ],
                    data=[],
                    page_current=0,
                    page_size=7,
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220, 220, 220)',
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold'
                    },
                    style_table={
                        'width': '100%',
                        # 'maxHeight': '300px',  # Hauteur fixe pour le contenu de la table
                        'minWidth': '100%',
                        'height': '100%', # Hauteur totale - hauteur du header
                        'minWidth': '100%',
                        'overflowY': 'hidden',
                        'overflowX': 'hidden'
                    },
                    style_cell={
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': 0,
                        'padding': '8px',
                        'textAlign': 'left'
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': 'employee'}, 'width': '15%'},
                        {'if': {'column_id': 'tache'}, 'width': '20%'},
                        {'if': {'column_id': 'manager'}, 'width': '15%'},
                        {'if': {'column_id': 'statut'}, 'width': '10%'},
                        {'if': {'column_id': 'progression'}, 'width': '10%'},
                        {'if': {'column_id': 'note'}, 'width': '10%'},
                        {'if': {'column_id': 'comments'}, 'width': '20%'}
                    ]
                ),
                style={"width": "100%", "height": "100%", "padding": "0"}
            )
        ],
        style={
            "display": "flex", 
            "flexDirection": "column", 
            "height": "100%", 
            "width": "100%", 
            # "overflow": "auto",
            "backgroundColor": "white", 
            "borderRadius": "15px", 
            "boxShadow": "4px 4px 15px rgba(0, 0, 0, 0.2)"
        }
    ),
    style={"height": "100%",}),
    style={"height": "370px", "overflow": "hidden",'borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
    className='mt-3'))  
        ]),id='content-col',style={'backgroundColor':'#F2F2F2','marginTop': '70px'})
        ],style={'backgroundColor':'#F2F2F2','overflow-x': 'hidden'},className='me-4 ms-2 mb-3 mt-3')
])



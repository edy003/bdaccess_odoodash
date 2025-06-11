from dash import html
import dash_mantine_components as dmc
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html,dcc 


layout=dbc.Row([
   
            # Sidebar fixe
            dbc.Col(
                html.Div([
                    html.Div(
                        [
                            html.Div('Filter', style={'color': 'white', 'fontSize': '16px'}),
                            html.Img(
                                src='/dash/assets/img/entonnoir.png',
                                style={
                                    'height': '20px',
                                    'marginLeft': 'auto'
                                }
                            ),
                        ],
                        style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'borderBottom': '2px solid white',
                            'marginTop': '8px',
                            'marginBottom': '20px',       
                        }
                    ),
                    dbc.Stack(
                        [
                            html.Div(id="dropdown_country"),
                            html.Div(id="sexe"),
                            html.Div(id="department"),
                        ],
                        gap=3,
                    ),
                ]),
                id='sidebar',
                width=2,
                style={
                    'backgroundColor': '#3a7a4f',
                    'height': '100vh',
                    'zIndex': '1000',
                    'position': 'fixed',
                    'left': '0',
                    'width': '16.666667%',
                    'top': '60px',
                    'paddingTop': '20px',
                    'paddingLeft': '15px',
                    'paddingRight': '15px'
                }
            ),
            
            # Contenu principal avec margin-left pour compenser la sidebar fixe
    dbc.Col(
    html.Div([
                    # KPIs Row
    dbc.Row([
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H3("Nombre d'employés", className="card-title text-center", style={'fontSize':'18px','color':'#285939'}),
                html.H1(id='kpi_employee', className="text-center", style={'color':'#8C1F1F'}),
            ], style={'padding-top': '5px', 'padding-bottom': '0px'}),
            className="h-100 border-0"
        ),
        style={'backgroundColor':'white', 'height': '95px', 'borderRadius': '15px', 'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},
        className="mx-2"
  ''  ),
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H3("Nombre d'hommes", className="card-title text-center", style={'fontSize':'18px','color':'#285939'}),
                html.H1(id='kpi_homme', className="text-center", style={'color':'#8C1F1F'}),
            ], style={'padding-top': '5px', 'padding-bottom': '0px'}),
            className="h-100 border-0"
        ),
        style={'backgroundColor':'white', 'height': '95px', 'borderRadius': '15px', 'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},
        className="mx-2"
    ),
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H3("Nombre de femmes", className="card-title text-center", style={'fontSize':'18px','color':'#285939'}),
                html.H1(id='kpi_femme', className="text-center", style={'color':'#8C1F1F'}),
            ], style={'padding-top': '5px', 'padding-bottom': '0px'}),
            className="h-100 border-0"
        ),
        style={'backgroundColor':'white', 'height': '95px', 'borderRadius': '15px', 'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},
        className="mx-2"
    ),
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H3("Nombre de projets", className="card-title text-center", style={'fontSize':'18px','color':'#285939'}),
                html.H1(id='kpi_projet', className="text-center", style={'color':'#8C1F1F'}),
            ], style={'padding-top': '5px', 'padding-bottom': '0px'}),
            className="h-100 border-0"
        ),
        style={'backgroundColor':'white', 'height': '95px', 'borderRadius': '15px', 'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},
        className="mx-2"
    ),
], className="g-3 align-items-stretch"),

                    
                    # Charts Row
                    dbc.Row([
                        dbc.Col([
                            html.Div(
                                dbc.Card([
                                    dbc.CardHeader(
                                        "Projet par statut",
                                        style={
                                            "padding": "5px", 
                                            "fontSize": "14px",
                                            "textAlign": "center",
                                            "height": "30px",
                                            'backgroundColor': '#3a7a4f',
                                            'color':'white',
                                            "fontSize": "14px",
                                            "fontWeight": 500,
                                            "lineHeight": "1.55",
                                        }
                                    ),
                                    dbc.CardBody(
                                        dcc.Graph(
                                            id='pie_statut',
                                            style={
                                                "width": "100%", 
                                                "height": "100%",
                                                "overflow":"hidden",
                                                'backgroundColor': '#3a7a4f',
                                                'color':'white',
                                                "fontSize": "14px",
                                                "fontWeight": 500,
                                                "lineHeight": "1.55",
                                            },
                                            config={'displayModeBar': False}
                                        ),
                                        style={"width": "100%", "height": "calc(100% - 30px)"}
                                    )
                                ], style={"height": "100%"}),
                                style={
                                    'height': '250px', 
                                    'width': '100%', 
                                    'overflow': 'hidden',
                                    'borderRadius': '15px',
                                    'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'
                                }
                            ),
                            html.Div(
                                dbc.Card([
                                    dbc.CardHeader(
                                        "Employe par genre",
                                        style={
                                            "padding": "5px", 
                                            "fontSize": "14px", 
                                            "height": "30px",
                                            "textAlign": "center",
                                            'backgroundColor': '#3a7a4f',
                                            'color':'white',
                                            "fontSize": "14px",
                                            "fontWeight": 500,
                                            "lineHeight": "1.55",
                                        }
                                    ),
                                    dbc.CardBody(
                                        dcc.Graph(
                                            id='pie_gender',
                                            style={"width": "100%", "height": "100%","overflow":"hidden"},
                                            config={'displayModeBar': False}
                                        ),
                                        style={"width": "100%", "height": "calc(100% - 30px)"}
                                    )
                                ], style={"height": "100%"}),
                                className="mt-3",
                                style={
                                    'height': '250px', 
                                    'width': '100%', 
                                    'overflow': 'hidden',
                                    'borderRadius': '15px',
                                    'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'
                                }
                            )
                        ], width=4),
                        
                        dbc.Col(
                            html.Div(
                                dbc.Card([
                                    dbc.CardHeader(
                                        "Employes par departement",
                                        style={
                                            "padding": "5px", 
                                            "fontSize": "14px", 
                                            "height": "30px",
                                            "textAlign": "center",
                                            'backgroundColor': '#3a7a4f',
                                            'color':'white',
                                            "fontSize": "14px",
                                            "fontWeight": 500,
                                            "lineHeight": "1.55",
                                        }
                                    ),
                                    dbc.CardBody(
                                        dcc.Graph(
                                            id='bar_employee',
                                            style={"width": "100%", "height": "100%","overflow":"hidden"},
                                            config={'displayModeBar': False}
                                        ),
                                        style={"width": "100%", "height": "calc(100% - 30px)"}
                                    )
                                ], style={"height": "100%",'overflow': 'hidden'}),
                                style={
                                    'height': 'auto', 
                                    'width': 'auto', 
                                    'overflow': 'hidden',
                                    'borderRadius': '15px',
                                    'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)',
                                    'position': 'relative',  # Position relative pour stabilité
                                    'flex': '1'
                                }
                            ),
                            className="ms-3",
                        ),
                    ], className="mt-3",style={
                    'overflow': 'hidden',           # Empêche tout débordement
                    'display': 'flex',             # Utilise flexbox
                    'flexWrap': 'nowrap',          # Empêche le retour à la ligne
             }),
                    
                    # Bottom Chart Row
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                dbc.Card([
                                    dbc.CardHeader(
                                        "Employes par pays",
                                        style={
                                            "padding": "5px", 
                                            "fontSize": "14px", 
                                            "height": "30px",
                                            'backgroundColor': '#3a7a4f',
                                            'color':'white',
                                            "fontSize": "14px",
                                            "fontWeight": 500,
                                            "lineHeight": "1.55",
                                            "textAlign": "center",
                                        }
                                    ),
                                    dbc.CardBody(
                                        dcc.Graph(
                                            id='bar_country',
                                            style={"width": "100%", "height": "100%","overflow":"hidden"},
                                            config={'displayModeBar': False}
                                        ),
                                        style={"width": "100%", "height": "calc(100% - 30px)"}
                                    )
                                ], style={"height": "100%",'overflow': 'hidden'}),
                                style={
                                    'height': '400px', 
                                    'width': '100%', 
                                    'overflow': 'hidden',
                                    'borderRadius': '15px',
                                    'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'
                                }
                            ),
                            className="mt-3"
                        )
                    ])
                ]),
                id='content-col',
                style={
                    'backgroundColor':'#F2F2F2',
                    'marginTop': '50px',
                    'marginLeft': '16.666667%',  # Compense la largeur de la sidebar fixe
                    'padding': '20px'
                }
            )
        ], 
        style={
            'backgroundColor':'#F2F2F2',
            'overflow-x': 'hidden'
        },
      
        className='me-2 ms-2 mb-3 mt-2')

# layout=html.Div(children=analyse_globale())
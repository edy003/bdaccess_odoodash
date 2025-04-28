from dash import Dash, html,dcc ,callback, Input, Output
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash
from app import employee_project


dash.register_page(__name__, path="/",order=1)


dropdown_country=  html.Div([
        "Country",
        dcc.Dropdown(employee_project['country_id'].unique(), id='dropdown_country')
    ])

option_gender = employee_project['gender'].unique()
option_department = employee_project['department_id'].unique()

sexe = dmc.MantineProvider(
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
        html.Div("Sexe"),
        # Conteneur pour gérer l'affichage vertical
        html.Div(
            dmc.ChipGroup(
                id="sexe",
                multiple=True,
                value=[],
                children=[
                    dmc.Chip(
                        gender,
                        value=gender,
                        variant="filled",
                        color="blue",
                        radius="md",
                        size="sm",
                        className="custom-chip"
                    )
                    for gender in option_gender
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

sexe = dmc.MantineProvider(
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
        html.Div("Sexe"),
        # Conteneur pour gérer l'affichage vertical
        html.Div(
            dmc.ChipGroup(
                id="sexe",
                multiple=True,
                value=[],
                children=[
                    dmc.Chip(
                        gender,
                        value=gender,
                        variant="filled",
                        color="blue",
                        radius="md",
                        size="sm",
                        className="custom-chip"
                    )
                    for gender in option_gender
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
                id="department",
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



layout=html.Div(children=[
        # dcc.Store(id='sidebar-state', data=True),
        dbc.Row([
            dbc.Col(dbc.Row(dbc.Col(html.Div([
            dbc.Stack(
            [
                html.Div(dropdown_country),
                html.Div(sexe),
                html.Div(department),
            ],
            gap=3,
        ),
            ])),align="center",className="h-100"),id='sidebar',width=2,
                    style={'backgroundColor': '#587362','height': '100vh','zIndex': '1000','position':'fixed','left':'0','width': '16.666667%','top':'60px'}),
            dbc.Col(id='spacer-col',width=2,style={'backgroundColor': '#F2F2F2','marginTop':'60px'}),
            dbc.Col(html.Div([
            dbc.Row([
            dbc.Col(html.Div(dbc.Card(
            dbc.CardBody(
            [
            html.H3("Nombre d'employes", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
            html.H1(id='kpi_employee',className="text-center",style={'color':'#8C1F1F'}),
            ],style={
                'padding-top': '5px',  # Réduit l'espace en haut
                'padding-bottom': '0px',
                
            }
            )
            ,className="w-100 h-100 border-0",style={'margin': '0', 'padding': '0'})),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
            dbc.Col(dbc.Card(
            dbc.CardBody(
            [
            html.H3("Nombre d'hommes", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
            html.H1(id='kpi_homme',className="text-center",style={'color':'#8C1F1F'}),
            ],style={
                'padding-top': '5px',  # Réduit l'espace en haut
                'padding-bottom': '0px',    
            }
            )
            ,className="w-100 h-100 border-0"),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},className="me-3 ms-3"),
            dbc.Col(dbc.Card(
            dbc.CardBody(
            [
            html.H3("Nombre de femmes", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
            html.H1(id='kpi_femme',className="text-center",style={'color':'#8C1F1F'}),
            ],style={
                'padding-top': '5px',  # Réduit l'espace en haut
                'padding-bottom': '0px',    
            }
            )
            ,className="w-100 h-100 border-0"),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
            dbc.Col(html.Div(dbc.Card(
            dbc.CardBody(
            [
            html.H3("Nombre de projets", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
            html.H1(id='kpi_projet',className="text-center",style={'color':'#8C1F1F'}),
            ],style={
                'padding-top': '5px',  # Réduit l'espace en haut
                'padding-bottom': '0px',    
            }
            ,className="w-100")
            ,className="w-100 h-100 border-0")),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},className="w-100 ms-3"),
            ]),
            dbc.Row([
            dbc.Col([
            html.Div(dbc.Card(
             [
             dbc.CardHeader(
            "Projet par statut",
            style={"padding": "5px", "fontSize": "14px", "height": "30px"}  # Ajuste ici selon besoin
            ),
            dbc.CardBody(
            dcc.Graph(id='pie_statut',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False})
            ,style={"width": "100%", "height": "calc(100% - 30px)"}
           )
           ],style={"height": "100%"}
           ),style={'height': '250px', 'width': '100%', 
                    'overflow': 'hidden','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
            html.Div((dbc.Card(
             [
             dbc.CardHeader(
            "Employe par genre",
            style={"padding": "5px", "fontSize": "14px", "height": "30px"}  # Ajuste ici selon besoin
            ),
            dbc.CardBody(
            dcc.Graph(id='pie_gender',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False})
            ,style={"width": "100%", "height": "calc(100% - 30px)"}
           )
           ],style={"height": "100%"}
           )),className="mt-3",style={'height': '250px', 'width': '100%', 
            'overflow': 'hidden','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'})
                ],width=4),
            dbc.Col( html.Div(dbc.Card(
             [
             dbc.CardHeader(
            "Employes par departement",
            style={"padding": "5px", "fontSize": "14px", "height": "30px"}  # Ajuste ici selon besoin
            ),
            dbc.CardBody(
            dcc.Graph(id='bar_employee',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False}),
            style={"width": "100%", "height": "calc(100% - 30px)"}
           )
           ],style={"height": "100%",'overflow': 'hidden'}
           ),style={'height': 'auto', 'width': '100%', 
                    'overflow': 'hidden','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),className="ms-3"),
            ],className="mt-3"),
            dbc.Row([
            dbc.Col(html.Div(dbc.Card(
             [
             dbc.CardHeader(
            "Employes par pays",
            style={"padding": "5px", "fontSize": "14px", "height": "30px"}  # Ajuste ici selon besoin
            ),
            dbc.CardBody(
            dcc.Graph(id='bar_country',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False}),
            style={"width": "100%", "height": "calc(100% - 30px)"}
           )
           ],style={"height": "100%",'overflow': 'hidden'}
           ),style={'height': '400px', 'width': '100%', 
                    'overflow': 'hidden','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),className="mt-3")

            ])
            ],id='content-col',),style={'backgroundColor':'#F2F2F2','marginTop': '70px'})
        ],style={'backgroundColor':'#F2F2F2','overflow-x': 'hidden'},className='me-4 ms-4 mb-3 mt-3')
       
    ])
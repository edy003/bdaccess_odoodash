# from dash import Dash, html,dcc,Input, Output,dash_table
# import dash_bootstrap_components as dbc
# import dash_mantine_components as dmc
# import dash
# import pandas as pd
# from widget import card
# import dash_ag_grid as dag
# from app import employee_valid_rating




# dash.register_page(__name__,order=2)

# columnDefs = [
#     {
#         "headerName": "Details de l'Evaluation",
#         "children": [
#             {"field": "Employee", "width": 180},
#             {"field": "Projet", "width": 200,"tooltipField": "projet"},
#             {"field": "Tache", "width":200,"tooltipField": "Tache"},
#             {"field":"Manager","width":180},
#             #  {
#             #     "field": "Statut",
#             #     "width": 120,
#             #     "cellRenderer": "StatusBadge",
#             #     "cellStyle": {
#             #         "paddingTop": "2px",
#             #         "paddingBottom": "4px"
#             #     }
#             # },
#             {"field": "Note", "width": 95,"cellRenderer": "NoteColor" },
#             {"field": "Commentaire", "width":300},
          
#         ],
#     },
# ]


# option_department = employee_valid_rating['department_id_y'].unique()

# dropdown_employee=  html.Div([
#         html.Div("employee",style={'color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",}),
#         dcc.Dropdown(employee_valid_rating['employee_name'].unique(), id='dropdown_employee')
#     ])



# date_min = employee_valid_rating['start_date_x'].min()
# date_max = employee_valid_rating['start_date_x'].max()

# date_range= dmc.MantineProvider(
#     theme={
#         "colorScheme": "light",
#         "primaryColor": "mygreen",
#         "colors": {
#         "mygreen": [
#             "#e6f0eb", "#cce0d6", "#99c1ad", "#66a384",
#             "#33845b", "#285939", "#1f452d", "#163021",
#             "#0d1c14", "#050d09"
#         ]
#     },
#         "components": {
#             "DatePickerInput": {
#                 "styles": {
#                     "dropdown": {"zIndex": '9999'},
#                     "input": {"zIndex": '9999'},
#                     "label": {"color": "white"}
#                 }
#             }
#         }
#     },
#     children=html.Div(
#         [
#             dmc.DatePickerInput(
#                 id="date-input",
#                 label="Date Range",
#                 minDate=date_min,
#                 maxDate=date_max,
#                 type="range",
#                 value=[date_min, date_max],
#                 valueFormat="YYYY-MM-DD",
#                 maw=300,
#             ),
#         ]
#     )
# )





# department = dmc.MantineProvider(
#     theme={"components": {
#         "Chip": {
#             "styles": {
#                 "label": {
#                     "width": "100%",  # Prend toute la largeur disponible
#                     "justifyContent": "center",
#                     "alignItems": "center",  
#                     "padding": "8px 12px"  # Padding supplémentaire pour l'esthétique
#                 },
#                 "input": {
#                         ":checked + label": {  # Ciblage du label lorsque l'input est coché
#                             "backgroundColor": "#228BE6 !important",
#                             "color": "white !important"
#                         }
#                     },
#                 "checkIcon": {
#                     "display": "none"  # Cache l'icône de coche
#                 }
#             }
#         }
#     }},
#     children=[
#         html.Div("Department",style={'color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",}),
#         # Conteneur pour gérer l'affichage vertical
#         html.Div(
#             dmc.ChipGroup(
#                 id="department1",
#                 multiple=True,
#                 value=[],
#                 children=[
#                     dmc.Chip(
#                         department,
#                         value=department,
#                         variant="filled",
#                         color="blue",
#                         radius="md",
#                         size="sm",
#                         className="custom-chip"
#                     )
#                     for department in option_department
#                 ]
#             ),
#             style={
#                 "width": "100%", 
#                 "display": "flex",
#                 "flexDirection": "column",  # Affichage en colonne
#                 "gap": "10px"  # Espacement entre les boutons
#             }
#         )
#     ]
# )


# # Layout obligatoire
# layout = html.Div(children=[
#         # dcc.Store(id='sidebar-state', data=True),
#         dbc.Row([
#             dbc.Col(dbc.Row(dbc.Col(html.Div([
#             html.Div(
#     [
#         html.Div('Filter', style={'color': 'white', 'fontSize': '16px'}),
#         html.Img(
#             src='dash/assets/img/entonnoir.png',  # Remplace par le chemin correct de ton image
#             style={
#                 'height': '20px',
#                 'marginLeft': 'auto'
#             }
#         ),
#     ],
#     style={
#         'display': 'flex',
#         'alignItems': 'center',
#         'justifyContent': 'space-between',
#         'borderBottom': '2px solid white',
#         'marginTop': '8px',
#         'marginBottom': '20px',       
#     }
#    ),
#             dbc.Stack(
#             [
#                 html.Div(date_range),
#                 html.Div(department),
#                 html.Div(dropdown_employee),
#             ],
#             gap=3,
#         ),
#             ])),),id='sidebar',width=2,
#                     style={'backgroundColor': '#3a7a4f','height': '100vh','zIndex': '300','position':'fixed','left':'0','width': '16.666667%','top':'60px'}),
#         dbc.Col(id='spacer-col',width=2,style={'backgroundColor': '#F2F2F2','marginTop':'60px'}),
#         dbc.Col(html.Div([
#         dbc.Row([
#         dbc.Col(card,width=4),
#         dbc.Col(html.Div(dbc.Card(
#         dbc.CardBody(
#         [
#         html.H3("Projets Affectes", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
#         html.H1(id='nbre_projet',className="text-center",style={'color':'#8C1F1F'}),
#         ],style={
#         'padding-top': '5px',  # Réduit l'espace en haut
#         'padding-bottom': '0px',    
#             }
#         ,className="w-100")
#         ,className="w-100 h-100 border-0")),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},className='ms-3 me-3'),
#         dbc.Col(html.Div(dbc.Card(
#         dbc.CardBody(
#         [
#         html.H3("Taches assignees", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
#         html.H1(id='nbre_tache',className="text-center",style={'color':'#8C1F1F'}),
#         ],style={
#         'padding-top': '5px',  # Réduit l'espace en haut
#         'padding-bottom': '0px',    
#         }
#         ,className="w-100")
#         ,className="w-100 h-100 border-0")),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},className='me-3'),
#         dbc.Col(html.Div(dbc.Card(
#         dbc.CardBody(
#         [
#         html.H3("Delai moyen", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
#         html.Div(id='date_delai',className="text-center",),
#         ],style={
#         'padding-top': '5px',  # Réduit l'espace en haut
#         'padding-bottom': '0px',    
#         }
#         ,className="w-100")
#         ,className="w-100 h-100 border-0")),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
#         ],style={}, className=''),
#         html.Div(dbc.Row([
#         dbc.Col(html.Div(dbc.Card(
#              [
#              dbc.CardHeader(
#             "Note moyenne",
#             style={"padding": "5px", "fontSize": "14px", "height": "30px",'backgroundColor': '#3a7a4f','color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55","textAlign": "center",}  # Ajuste ici selon besoin
#             ),
#             dbc.CardBody(
#             dcc.Graph(id='taux_satisfaction',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False})
#             ,style={"width": "100%", "height": "calc(100% - 30px)"}
#            )
#            ],style={"height": "100%",'width':'100%'}
#            ),style={'height':'250px','backgroundColor':'white','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),width=6,className='me-3'),
#         dbc.Col(html.Div(dbc.Card(
#              [
#              dbc.CardHeader(
#             "Tache completes",
#             style={"padding": "5px", "fontSize": "14px", "height": "30px",'backgroundColor': '#3a7a4f','color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55","textAlign": "center",}  # Ajuste ici selon besoin
#             ),
#             dbc.CardBody(
#             dcc.Graph(id='taux_task',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False}),
#             style={"width": "100%", "height": "calc(100% - 30px)"}
#            )
#            ],style={"height": "100%",'width':'100%'}
#            ),style={'height':'250px','overflow':'hidden','backgroundColor':'white','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),width=True),
#         ],className='mt-3',style={'overflowX':'hidden'})),

    
#     dbc.Row(dbc.Col(html.Div([
#          dag.AgGrid(
#                     id="column-groups-note",
#                     # className="ag-theme-alpine color-fonts",
#                     rowData=[],
#                     columnDefs=columnDefs,
#                     defaultColDef={"filter": True,"headerClass": "centered-header"},
#                     dashGridOptions={"animateRows": False,
#                     # "domLayout": "autoHeight",
#                     "pagination": True,            
#                     "paginationPageSize": 8},
#                     className="ag-theme-alpine",
#                     style={"height": "calc(100% - 50px)"}
                   
#                 )
       
#          ],style={"height": "100%",'display': 'flex','flexDirection': 'column','justifyContent': 'center','width': '100%'}, className='mt-4'),
    
#     style={"height": "100%"}),style={"height": "550px",'overflow':'hidden'})

#         ]),id='content-col',style={'backgroundColor':'#F2F2F2','marginTop': '70px'})
#         ],style={'backgroundColor':'#F2F2F2','overflow-x': 'hidden'},className='me-2 ms-2 mb-3 mt-3')
# ])



import dash
import dash_bootstrap_components as dbc
from dash import Dash, html,dcc,Input, Output,dash_table
import dash_ag_grid as dag


columnDefs = [
    {
        "headerName": "Details de l'Evaluation",
        "children": [
            {"field": "Employee", "width": 180},
            {"field": "Projet", "width": 200,"tooltipField": "projet"},
            {"field": "Tache", "width":200,"tooltipField": "Tache"},
            {"field":"Manager","width":180},
            #  {
            #     "field": "Statut",
            #     "width": 120,
            #     "cellRenderer": "StatusBadge",
            #     "cellStyle": {
            #         "paddingTop": "2px",
            #         "paddingBottom": "4px"
            #     }
            # },
            {"field": "Note", "width": 95,"cellRenderer": "NoteColor" },
            {"field": "Commentaire", "width":300},
          
        ],
    },
]




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
                            html.Div(id="department1"),
                            html.Div(id="dropdown_employee"),
                            html.Div(id="date-input"),
                        ],
                        gap=3,
                    ),
                ]),
                id='sidebar',
                width=2,
                style={
                    'backgroundColor': '#3a7a4f',
                    'height': '100vh',
                    'zIndex': '100',
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
                html.H3(id='employee_name', className="card-title text-center ", style={'fontSize':'18px','color':'#285939'}),
                html.H3(id='employee_department', className="card-title text-center", style={'fontSize':'18px','color':'#8C1F1F'}),
            ], style={'padding-top': '5px', 'padding-bottom': '0px','display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'center', 'height': '100%'}),
            className="h-100 border-0"
        ),
        style={'backgroundColor':'white', 'height': '95px', 'borderRadius': '15px', 'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},
        className="mx-2"
  ''  ),
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H3("Projets Affectes", className="card-title text-center", style={'fontSize':'18px','color':'#285939'}),
                html.H1(id='nbre_projet', className="text-center", style={'color':'#8C1F1F'}),
            ], style={'padding-top': '5px', 'padding-bottom': '0px'}),
            className="h-100 border-0"
        ),
        style={'backgroundColor':'white', 'height': '95px', 'borderRadius': '15px', 'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},
        className="mx-2"
    ),
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H3("Taches assignees", className="card-title text-center", style={'fontSize':'18px','color':'#285939'}),
                html.H1(id='nbre_tache', className="text-center", style={'color':'#8C1F1F'}),
            ], style={'padding-top': '5px', 'padding-bottom': '0px'}),
            className="h-100 border-0"
        ),
        style={'backgroundColor':'white', 'height': '95px', 'borderRadius': '15px', 'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},
        className="mx-2"
    ),
    dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H3("Delai moyen", className="card-title text-center", style={'fontSize':'18px','color':'#285939'}),
                html.Div(id='date_delai', className="text-center", style={'color':'#8C1F1F'}),
            ], style={'padding-top': '5px', 'padding-bottom': '0px'}),
            className="h-100 border-0"
        ),
        style={'backgroundColor':'white', 'height': '95px', 'borderRadius': '15px', 'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},
        className="mx-2"
    ),
], className="g-3 align-items-stretch"),

                    
    # Charts Row
    dbc.Row([
    dbc.Col(html.Div(
                dbc.Card([
                    dbc.CardHeader(
                        "Note moyenne",
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
                            id='taux_satisfaction',
                            style={"width": "100%", "height": "100%","overflow":"hidden"},
                            config={'displayModeBar': False}
                            ),
                            style={"width": "100%", "height": "calc(100% - 30px)"}
                                )
                            ], style={"height": "100%",'overflow': 'hidden'}),
                            style={
                                'height': '250px', 
                                'width': '100%', 
                                'overflow': 'hidden',
                                'borderRadius': '15px',
                                'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'
                                }
                            ),className="me-3"),
    dbc.Col(html.Div(
                dbc.Card([
                    dbc.CardHeader(
                        "Tache completes",
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
                            id='taux_task',
                            style={"width": "100%", "height": "100%","overflow":"hidden"},
                            config={'displayModeBar': False}
                            ),
                            style={"width": "100%", "height": "calc(100% - 30px)"}
                                )
                            ], style={"height": "100%",'overflow': 'hidden'}),
                            style={
                                'height': '250px', 
                                'width': '100%', 
                                'overflow': 'hidden',
                                'borderRadius': '15px',
                                'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'
                                }
                            ))    
                        
    ], className="mt-3",style={
                    'overflow': 'hidden',           # Empêche tout débordement
                    'display': 'flex',             # Utilise flexbox
                    'flexWrap': 'nowrap',          # Empêche le retour à la ligne
             }),
                    
                    # Bottom Chart Row
    dbc.Row([
        dbc.Col(
            html.Div([
                dag.AgGrid(
                    id="column-groups-note",
                    # className="ag-theme-alpine color-fonts",
                    rowData=[],
                    columnDefs=columnDefs,
                    defaultColDef={"filter": True,"headerClass": "centered-header"},
                    dashGridOptions={"animateRows": False,
                    # "domLayout": "autoHeight",
                    "pagination": True,            
                    "paginationPageSize": 9},
                    className="ag-theme-alpine",
                    style={"height": "100%"}
                   
                )
       

            ],style={
                'height': '550px', 
                'width': '100%', 
                'overflow': 'hidden',
                'borderRadius': '15px',
                'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'
                }
                )
                )
                    ],className="mt-3")
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




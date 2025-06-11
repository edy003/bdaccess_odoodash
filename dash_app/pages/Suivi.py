# import dash
# from dash import html
# import dash_mantine_components as dmc
# import dash_ag_grid as dag
# from dash import Input, Output, html, callback,dcc
# import dash_bootstrap_components as dbc
# from app import employee_suivi

# dash.register_page(__name__,order=3)





# columnDefs = [
#     {
#         "headerName": "Details des taches",
#         "children": [
#             {"field": "Employee", "width": 180},
#             {"field": "Manager", "width": 180},
#             {"field": "projet", "width": 200, "tooltipField": "projet"},
#             {"field": "Tache", "width": 200, "tooltipField": "Tache"},
#             {"field": "Description", "width": 300, "tooltipField": "Description"},
#             {"field": "Priorite", "width": 95},
#             {
#             "field": "Progression",
#             "width": 250,
#             "cellRenderer": "ProgressBar"
             
#            },
#             {"field": "Statut", "width": 150, "cellRenderer": "StatusBadgesuivi",
#                 "cellStyle": {
#                     "paddingTop": "2px",
#                     "paddingBottom": "4px"
#                 }},
#             {"field": "sous taches", "width": 120, "filter": "agNumberColumnFilter", "columnGroupShow": "closed"},
#         ]
#     }
# ]



# defaultColDef = {
#     "filter": True,
#     "wrapText": True,  # Permet au texte de s'afficher sur plusieurs lignes
#     "autoHeight": True,  # Ajuste automatiquement la hauteur en fonction du contenu
#     "cellStyle": {"white-space": "normal"},  # Empêche la troncature du texte
#     "headerClass": "centered-header"  # Classe CSS pour centrer les en-têtes
# }





# option_department = employee_suivi['department_id_y'].dropna().unique()


# dropdown_employee=  html.Div([
#         html.Div("employee",style={'color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",}),
#         dcc.Dropdown(employee_suivi['employee_name'].unique(), id='dropdown_employee2')
#     ])

# date_min = employee_suivi['start_date_x'].min()
# date_max = employee_suivi['start_date_x'].max()

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
#                 id="date-input2",
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
#                 id="department2",
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
#         dag.AgGrid(
#                     id="column-groups-basic",
#                     # className="ag-theme-alpine color-fonts",
#                     rowData=[],
#                     columnDefs=columnDefs,
#                     defaultColDef={"filter": True,"headerClass": "centered-header"},
#                     dashGridOptions={"animateRows": False,
#                     # "domLayout": "autoHeight",
#                     "pagination": True,            
#                     "paginationPageSize": 8},
#                     dangerously_allow_code=True,
#                     className="ag-theme-alpine",
#                     style={"height": "calc(100% - 50px)"}
#                 )
#          ], style={'display': 'flex','flexDirection': 'column','justifyContent': 'center','height': '550px'}),
#         id='content-col',style={'backgroundColor':'#F2F2F2','marginTop': '60px','height': 'calc(100vh - 60px)'})
#         ],style={'backgroundColor':'#F2F2F2','overflow':'hidden'},className='me-2 ms-2')
#      ],style={'overflow':'hidden','height': '100vh'})

from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_ag_grid as dag


columnDefs = [
    {
        "headerName": "Details des taches",
        "children": [
            {"field": "Employee", "width": 180},
            {"field": "Manager", "width": 180},
            {"field": "projet", "width": 200, "tooltipField": "projet"},
            {"field": "Tache", "width": 200, "tooltipField": "Tache"},
            {"field": "Description", "width": 300, "tooltipField": "Description"},
            {"field": "Priorite", "width": 95},
            {
            "field": "Progression",
            "width": 250,
            "cellRenderer": "ProgressBar"
             
           },
            {"field": "Statut", "width": 150, "cellRenderer": "StatusBadgesuivi",
                "cellStyle": {
                    "paddingTop": "2px",
                    "paddingBottom": "4px"
                }},
            {"field": "sous taches", "width": 120, "filter": "agNumberColumnFilter", "columnGroupShow": "closed"},
        ]
    }
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
                            html.Div(id="department2"),
                            html.Div(id="dropdown_employee2"),
                            html.Div(id="date-input2"),
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
    dbc.Row([
        dbc.Col(
            html.Div([
                dag.AgGrid(
                    id="column-groups-basic",
                    # className="ag-theme-alpine color-fonts",
                    rowData=[],
                    columnDefs=columnDefs,
                    defaultColDef={"filter": True,"headerClass": "centered-header"},
                    dashGridOptions={"animateRows": False,
                    # "domLayout": "autoHeight",
                    "pagination": True,            
                    "paginationPageSize": 9},
                    dangerously_allow_code=True,
                    className="ag-theme-alpine",
                    style={"height": "100%"}
                   
                )
       

            ],style={
                'height': '550px', 
                'width': '100%', 
                'overflow': 'hidden',
                'borderRadius': '15px',
                'boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)',
                'display': 'flex','flexDirection': 'column','justifyContent': 'center',
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





# from dash import Dash, html,dcc ,callback, Input, Output
# import dash_bootstrap_components as dbc
# import dash_mantine_components as dmc
# import dash
# from app import employee_project_valid


# dash.register_page(__name__, path="/",order=1)


# dropdown_country=  html.Div([
#         html.Div("Country",style={'color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",}),
#         dcc.Dropdown(employee_project_valid['country_id'].unique(), id='dropdown_country')
#     ])

# option_gender = employee_project_valid['gender'].unique()
# option_department = employee_project_valid['department_id'].unique()

# # sexe = dmc.MantineProvider(
# #     theme={"components": {
# #         "Chip": {
# #             "styles": {
# #                 "label": {
# #                     "width": "100%",  # Prend toute la largeur disponible
# #                     "justifyContent": "center",
# #                     "alignItems": "center",  
# #                     "padding": "8px 12px"  # Padding supplémentaire pour l'esthétique
# #                 },
# #                 "input": {
# #                         ":checked + label": {  # Ciblage du label lorsque l'input est coché
# #                             "backgroundColor": "#228BE6 !important",
# #                             "color": "white !important"
# #                         }
# #                     },
# #                 "checkIcon": {
# #                     "display": "none"  # Cache l'icône de coche
# #                 }
# #             }
# #         }
# #     }},
# #     children=[
# #         html.Div("Sexe"),
# #         # Conteneur pour gérer l'affichage vertical
# #         html.Div(
# #             dmc.ChipGroup(
# #                 id="sexe",
# #                 multiple=True,
# #                 value=[],
# #                 children=[
# #                     dmc.Chip(
# #                         gender,
# #                         value=gender,
# #                         variant="filled",
# #                         color="blue",
# #                         radius="md",
# #                         size="sm",
# #                         className="custom-chip"
# #                     )
# #                     for gender in option_gender
# #                 ]
# #             ),
# #             style={
# #                 "width": "100%", 
# #                 "display": "flex",
# #                 "flexDirection": "column",  # Affichage en colonne
# #                 "gap": "10px"  # Espacement entre les boutons
# #             }
# #         )
# #     ]
# # )

# sexe = dmc.MantineProvider(
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
#         html.Div("Sexe",style={'color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",}),
#         # Conteneur pour gérer l'affichage vertical
#         html.Div(
#             dmc.ChipGroup(
#                 id="sexe",
#                 multiple=True,
#                 value=[],
#                 children=[
#                     dmc.Chip(
#                         gender,
#                         value=gender,
#                         variant="filled",
#                         color="blue",
#                         radius="md",
#                         size="sm",
#                         className="custom-chip"
#                     )
#                     for gender in option_gender
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
#                 id="department",
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



# layout=html.Div(children=[
#    
#         dbc.Row([
#             dbc.Col(dbc.Row(dbc.Col(html.Div([
#                  html.Div(
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
#                 html.Div(dropdown_country),
#                 html.Div(sexe),
#                 html.Div(department),
#             ],
#             gap=3,
#         ),
#             ]))),id='sidebar',width=2,
#             style={'backgroundColor': '#3a7a4f','height': '100vh','zIndex': '1000','position':'fixed','left':'0','width': '16.666667%','top':'60px'}),
#             dbc.Col(id='spacer-col',width=2,style={'backgroundColor': '#F2F2F2','marginTop':'60px'}),
#             dbc.Col(html.Div([
#             dbc.Row([
#             dbc.Col(html.Div(dbc.Card(
#             dbc.CardBody(
#             [
#             html.H3("Nombre d'employes", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
#             html.H1(id='kpi_employee',className="text-center",style={'color':'#8C1F1F'}),
#             ],style={
#                 'padding-top': '5px',  # Réduit l'espace en haut
#                 'padding-bottom': '0px',
                
#             }
#             )
#             ,className="w-100 h-100 border-0",style={'margin': '0', 'padding': '0'})),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
#             dbc.Col(dbc.Card(
#             dbc.CardBody(
#             [
#             html.H3("Nombre d'hommes", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
#             html.H1(id='kpi_homme',className="text-center",style={'color':'#8C1F1F'}),
#             ],style={
#                 'padding-top': '5px',  # Réduit l'espace en haut
#                 'padding-bottom': '0px',    
#             }
#             )
#             ,className="w-100 h-100 border-0"),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},className="me-3 ms-3"),
#             dbc.Col(dbc.Card(
#             dbc.CardBody(
#             [
#             html.H3("Nombre de femmes", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
#             html.H1(id='kpi_femme',className="text-center",style={'color':'#8C1F1F'}),
#             ],style={
#                 'padding-top': '5px',  # Réduit l'espace en haut
#                 'padding-bottom': '0px',    
#             }
#             )
#             ,className="w-100 h-100 border-0"),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
#             dbc.Col(html.Div(dbc.Card(
#             dbc.CardBody(
#             [
#             html.H3("Nombre de projets", className="card-title text-center",style={'fontSize':'18px','color':'#285939'}),
#             html.H1(id='kpi_projet',className="text-center",style={'color':'#8C1F1F'}),
#             ],style={
#                 'padding-top': '5px',  # Réduit l'espace en haut
#                 'padding-bottom': '0px',    
#             }
#             ,className="w-100")
#             ,className="w-100 h-100 border-0")),style={'backgroundColor':'white','height': '95px', 'width': '100%','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'},className="w-100 ms-3"),
#             ]),
#             dbc.Row([
#             dbc.Col([
#             html.Div(dbc.Card(
#              [
#              dbc.CardHeader(
#             "Projet par statut",
#             style={"padding": "5px", "fontSize": "14px","textAlign": "center", "height": "30px",'backgroundColor': '#3a7a4f','color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",}  # Ajuste ici selon besoin
#             ),
#             dbc.CardBody(
#             dcc.Graph(id='pie_statut',style={"width": "100%", "height": "100%","overflow":"hidden",'backgroundColor': '#3a7a4f','color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",},config={'displayModeBar': False})
#             ,style={"width": "100%", "height": "calc(100% - 30px)"}
#            )
#            ],style={"height": "100%"}
#            ),style={'height': '250px', 'width': '100%', 
#                     'overflow': 'hidden','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),
#             html.Div((dbc.Card(
#              [
#              dbc.CardHeader(
#             "Employe par genre",
#             style={"padding": "5px", "fontSize": "14px", "height": "30px","textAlign": "center",'backgroundColor': '#3a7a4f','color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",}  # Ajuste ici selon besoin
#             ),
#             dbc.CardBody(
#             dcc.Graph(id='pie_gender',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False})
#             ,style={"width": "100%", "height": "calc(100% - 30px)"}
#            )
#            ],style={"height": "100%"}
#            )),className="mt-3",style={'height': '250px', 'width': '100%', 
#             'overflow': 'hidden','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'})
#                 ],width=4),
#             dbc.Col( html.Div(dbc.Card(
#              [
#              dbc.CardHeader(
#             "Employes par departement",
#             style={"padding": "5px", "fontSize": "14px", "height": "30px","textAlign": "center",'backgroundColor': '#3a7a4f','color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55",}  # Ajuste ici selon besoin
#             ),
#             dbc.CardBody(
#             dcc.Graph(id='bar_employee',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False}),
#             style={"width": "100%", "height": "calc(100% - 30px)"}
#            )
#            ],style={"height": "100%",'overflow': 'hidden'}
#            ),style={'height': 'auto', 'width': '100%', 
#                     'overflow': 'hidden','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),className="ms-3"),
#             ],className="mt-3"),
#             dbc.Row([
#             dbc.Col(html.Div(dbc.Card(
#              [
#              dbc.CardHeader(
#             "Employes par pays",
#             style={"padding": "5px", "fontSize": "14px", "height": "30px",'backgroundColor': '#3a7a4f','color':'white',"fontSize": "14px","fontWeight": 500,"lineHeight": "1.55","textAlign": "center",}  # Ajuste ici selon besoin
#             ),
#             dbc.CardBody(
#             dcc.Graph(id='bar_country',style={"width": "100%", "height": "100%","overflow":"hidden"},config={'displayModeBar': False}),
#             style={"width": "100%", "height": "calc(100% - 30px)"}
#            )
#            ],style={"height": "100%",'overflow': 'hidden'}
#            ),style={'height': '400px', 'width': '100%', 
#                     'overflow': 'hidden','borderRadius': '15px','boxShadow': '4px 4px 15px rgba(0, 0, 0, 0.2)'}),className="mt-3")

#             ])
#             ],id='content-col',),style={'backgroundColor':'#F2F2F2','marginTop': '70px'})
#         ],style={'backgroundColor':'#F2F2F2','overflow-x': 'hidden'},className='me-2 ms-2 mb-3 mt-3')
       
#     ])






from dash import html, dash,dcc,callback,Input, Output
import dash
import dash_bootstrap_components as dbc
# dash.register_page(__name__, path="/",order=1)





layout=html.Div(
    [
    
    dcc.Location(id="url1", refresh=False),
    # html.Div(id='page'),
    dbc.Navbar(
    dbc.Container([
        dbc.Row([
            # Logo et burger à gauche
            dbc.Col(
                html.Div([
                    html.Img(
                        src="/dash/assets/img/logo_qualisys.png",
                        height="40px",
                        style={
                            "transform": "scale(2)",
                            "transformOrigin": "left center"
                        }
                    ),
                    html.Div()
                ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}),
                width="auto",
                className="me-auto"
            ),

            # Navigation à droite
            dbc.Col([
                dbc.Nav(
    [
        dbc.NavItem(
            dbc.NavLink("Analyse Globale", href="/analyse",id="nav-link-home")
        ),
        dbc.NavItem(
            dbc.NavLink("Performances", href="/performances",id="nav-link-performances")
        ),
        dbc.NavItem(
            dbc.NavLink("Suivi", href="/suivi",id="nav-link-suivi")
        ),
    ],
    navbar=True,
    pills=False,  # Style onglet actif plus visible
    className="nav-links ms-auto"
)
            ],
            width="auto")
        ],
        justify="between",
        className="w-100 align-items-center")
    ],
    fluid=True
    ),
    color=None,
    dark=False,
    style={
        "backgroundColor": "white",
        "borderBottom": "1px solid #eaeaea",
        "top": 0,
        "position": "fixed",
        "width": "100%",
        "zIndex": 1000,
        "height": "60px"
    },
),
html.Div(id='page'),
    ],
    style={
        'backgroundColor':'#F2F2F2',
        'overflow-x': 'hidden'
    },
      
)

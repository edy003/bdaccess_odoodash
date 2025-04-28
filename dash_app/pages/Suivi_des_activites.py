import dash
from dash import html
import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash import Input, Output, html, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__,order=3)


columnDefs = [
    {
        "headerName": "Details des taches",
        "children": [
            {"field": "Employee", "width": 180},
            {"field": "Manager", "width":180},
            {"field": "Tache", "width":200},
            {"field": "Description", "width": 300},
            {"field": "Priorite", "width": 95},
            {"field": "Progression", "width":80},
            {"field": "Statut", "width": 95},
        ],
    },
    {
        "headerName": "Details des sous tache",
        "children": [
            {"field": "total", "width":80, "filter": "agNumberColumnFilter", "columnGroupShow": "closed"},
            {"field": "Description", "width": 300, "filter": "agNumberColumnFilter", "columnGroupShow": "open"},
            {"field": "statut", "width": 95, "filter": "agNumberColumnFilter", "columnGroupShow": "open"},
        ],
    },
]





# option_department = employee_valid_rating['department_id'].unique()

# dropdown_employee=  html.Div([
#         "employee",
#         dcc.Dropdown(employee_valid_rating['name_x'].unique(), id='dropdown_employee')
#     ])

# cols_to_convert = ['start_date', 'expected_end_date', 'end_date', 'evaluation_date']
# for col in cols_to_convert:
#     employee_valid_rating.loc[:, col] = pd.to_datetime(employee_valid_rating[col], errors='coerce')
# employee_valid_rating = employee_valid_rating[employee_valid_rating['start_date'].notna()]
# date_min = employee_valid_rating['start_date'].min()
# date_max = employee_valid_rating['start_date'].max()

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
#                     "input": {"zIndex": '9999'}
#                 }
#             }
#         }
#     },
#     children=html.Div(
#         [
#             dmc.DatePickerInput(
#                 id="date-input",
#                 label="Date Range",
#                 description="Select a date range",
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
#         html.Div("Department"),
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


# Layout obligatoire
layout = html.Div(children=[
        # dcc.Store(id='sidebar-state', data=True),
        dbc.Row([
            dbc.Col(dbc.Row(dbc.Col(html.Div([
            dbc.Stack(
            [
                # html.Div(date_range),
                # html.Div(department),
                # html.Div(dropdown_employee),
            ],
            gap=3,
        ),
            ])),),id='sidebar',width=2,
                    style={'backgroundColor': '#587362','height': '100vh','zIndex': '300','position':'fixed','left':'0','width': '16.666667%','top':'60px'}),
        dbc.Col(id='spacer-col',width=2,style={'backgroundColor': '#F2F2F2','marginTop':'60px'}),
        dbc.Col(html.Div([
        dag.AgGrid(
                    id="column-groups-basic",
                    rowData=[],
                    columnDefs=columnDefs,
                    defaultColDef={"filter": True},
                    dashGridOptions={"animateRows": False},
                )
         ], style={'display': 'flex','flexDirection': 'column','justifyContent': 'center','height': '100%'}),
        id='content-col',style={'backgroundColor':'#F2F2F2','marginTop': '60px','height': 'calc(100vh - 60px)'})
        ],style={'backgroundColor':'#F2F2F2','overflow':'hidden'},className='me-2 ms-2')
     ],style={'overflow':'hidden','height': '100vh'})



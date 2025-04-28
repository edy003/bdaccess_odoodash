# -*- coding: utf-8 -*-
import sys
print("Python utilisé :", sys.executable)
import dash
from dash import html,dcc, Input, Output,State
import logging
import math
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import requests
from flask_caching import Cache
from widget import burger_component,create_pie_status,create_bar_chart,create_gauge_chart,create_gauge_task





_logger = logging.getLogger(__name__)

def get_employee_data():
        try:
        # Utilisez l'URL complète avec le port Odoo
            url = 'http://localhost:8069/get_employee_data'
            response = requests.get(url, headers={'Accept': 'application/json'})
        
            _logger.info(f"Statut de la réponse : {response.status_code}")
            _logger.info(f"Contenu de la réponse : {response.text}")
        
            if response.status_code == 200:
                return response.json()
            else:
                _logger.error(f"Erreur de requête : {response.status_code}")
            return []
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des données : {e}")
        return []
    
def get_employee_ratings():
        try:
            url = 'http://localhost:8069/get_employee_ratings'
            response = requests.get(url, headers={'Accept': 'application/json'})
        
            _logger.info(f"Statut de la réponse (ratings): {response.status_code}")
            _logger.info(f"Contenu de la réponse (ratings): {response.text}")

            if response.status_code == 200:
                return response.json()
            else:
                _logger.error(f"Erreur de requête (ratings) : {response.status_code}")
            return []
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des évaluations : {e}")
        return []
    
def get_project_deliveries():
        try:
            url = 'http://localhost:8069/get_project_deliveries'
            response = requests.get(url, headers={'Accept': 'application/json'})
        
            _logger.info(f"Statut de la réponse (deliveries): {response.status_code}")
            _logger.info(f"Contenu de la réponse (deliveries): {response.text}")

            if response.status_code == 200:
                return response.json()
            else:
                _logger.error(f"Erreur de requête (deliveries) : {response.status_code}")
            return []
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des livraisons : {e}")
        return []
    
def get_projects():
        try:
            url = 'http://localhost:8069/get_projects'
            response = requests.get(url, headers={'Accept': 'application/json'})
        
            _logger.info(f"Statut de la réponse (projets): {response.status_code}")
            _logger.info(f"Contenu de la réponse (projets): {response.text}")

            if response.status_code == 200:
               return response.json()
            else:
                _logger.error(f"Erreur de requête (projets) : {response.status_code}")
            return []
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des projets : {e}")
        return []
    
def get_tasks():
        try:
            url = 'http://localhost:8069/get_tasks'
            response = requests.get(url, headers={'Accept': 'application/json'})

            _logger.info(f"Statut de la réponse (tasks): {response.status_code}")
            _logger.info(f"Contenu de la réponse (tasks): {response.text}")

            if response.status_code == 200:
                return response.json()
            else:
                _logger.error(f"Erreur de requête (tasks) : {response.status_code}")
            return []
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des tâches : {e}")
        return []
    
def get_subtasks():
        try:
           url = 'http://localhost:8069/get_subtasks'
           response = requests.get(url, headers={'Accept': 'application/json'})

           _logger.info(f"Statut de la réponse (subtasks): {response.status_code}")
           _logger.info(f"Contenu de la réponse (subtasks): {response.text}")

           if response.status_code == 200:
               return response.json()
           else:
               _logger.error(f"Erreur de requête (subtasks) : {response.status_code}")
           return []
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des sous-tâches : {e}")
        return []




subtasks = get_subtasks()

if not subtasks:
     _logger.warning("Aucune sous-tâche récupérée")
     subtasks = []

subtasks_df = pd.DataFrame(subtasks)
print(subtasks_df.columns)


tasks = get_tasks()

if not tasks:
    _logger.warning("Aucune tâche récupérée")
    tasks = []

tasks_df = pd.DataFrame(tasks)
print(tasks_df.columns)

employee_ratings = get_employee_ratings()

if not employee_ratings:
    _logger.warning("Aucune évaluation récupérée")
    employee_ratings = []
ratings_df = pd.DataFrame(employee_ratings)
# print(ratings_df.columns)
    
project_deliveries = get_project_deliveries()

if not project_deliveries:
    _logger.warning("Aucune livraison de projet récupérée")
    project_deliveries = []
deliveries_df = pd.DataFrame(project_deliveries)
# print(deliveries_df.head())

employee_data = get_employee_data()

if not employee_data:
    _logger.warning("Aucune donnée d'employé n'a été récupérée")
    employee_data = []
employee = pd.DataFrame(employee_data)
print(employee.columns)

project_data = get_projects()

if not project_data:
    _logger.warning("Aucun projet récupéré")
    project_data = []
projects = pd.DataFrame(project_data)
# print(projects.head())


employee_project = employee.merge(projects, on='department_id', how='outer')

employee_task = employee.merge(tasks_df, left_index=True, right_on='employee',how='outer')
employee_task_rating = employee_task.merge(ratings_df,on='employee',how='outer')
employee_valid_rating=employee_task_rating[employee_task_rating['id'].notna()].copy()
employee_valid_rating['start_date']=pd.to_datetime(employee_valid_rating['start_date'])
employee_valid_rating['expected_end_date']=pd.to_datetime(employee_valid_rating['expected_end_date'])
employee_valid_rating['end_date']=pd.to_datetime(employee_valid_rating['end_date'])
employee_valid_rating = employee_valid_rating[employee_valid_rating['start_date'].notna()]

employee_t = employee.merge(tasks_df,left_on='id',right_on='tache_id',how='outer')
employee_suivi = employee_t.merge(subtasks_df,left_on='tache_id',right_on='id',how='outer')
print(employee_suivi.head())

# print(employee_valid_rating.info())




def create_dash_app():

    """Créer et configurer l'application Dash"""
    app = dash.Dash(
        __name__,
        requests_pathname_prefix='/dash/',  # Corrige les erreurs de chemin derrière Nginx
        routes_pathname_prefix='/dash/',    # Corrige le loading infini
        assets_url_path='/dash/assets',
        use_pages=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP,dmc.styles.DATES],
        suppress_callback_exceptions=True    # Corrige le chargement des fichiers statiques
    )
    cache = Cache()
    cache.init_app(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './cache-directory',
    'CACHE_DEFAULT_TIMEOUT': 300
   })

    
    # Layout simple
    app.layout = html.Div(
    [
    dbc.Navbar(
    dbc.Container([
        dbc.Row([
            # Logo et burger à gauche
            dbc.Col(
                html.Div([
                    html.Img(
                        src="dash/assets/img/logo_qualisys.png",
                        height="40px",
                        style={
                            "transform": "scale(2)",
                            "transformOrigin": "left center"
                        }
                    ),
                    html.Div(burger_component)
                ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}),
                width="auto",
                className="me-auto"
            ),

            # Navigation à droite
            dbc.Col([
                dcc.Location(id="url", refresh=True),
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                page["name"],
                                href=page["relative_path"],
                                id=f"nav-{page['module'].split('.')[-1]}",
                                active="exact"
                            )
                        )
                        for page in dash.page_registry.values()
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
dash.page_container
          
          ],
          style={'backgroundColor':'#F2F2F2','overflow-x': 'hidden'}
    )
    

    
    def filter_data(df, dropdown_country=None, sexe=None, department=None):
    # Appliquer tous les filtres en une seule fois avec une approche conditionnelle
        mask = pd.Series(True, index=df.index)
    
        if dropdown_country:
            mask &= (df["country_id"] == dropdown_country)
    
        if sexe:
            mask &= df["gender"].isin(sexe)
    
        if department:
            mask &= df["department_id"].isin(department)
    
        return df[mask]
    
    # Décorateur de mise en cache (à utiliser avec Flask-Caching)
    @cache.memoize()
    def get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple):
       """Récupère et filtre les données avec mise en cache"""
        # Convertir les tuples en listes pour le filtrage
       sexe = list(sexe_tuple) if sexe_tuple else None
       department = list(department_tuple) if department_tuple else None
       return filter_data(employee_project, dropdown_country, sexe, department)
    

    def filter_data_performance(df, dropdown_employee=None, department1=None, start_date=None, end_date=None):
    # Initialiser un masque avec True
        mask = pd.Series(True, index=df.index)

        if dropdown_employee:
            mask &= (df["name_x"] == dropdown_employee)

        if department1:
            mask &= df["department_id"].isin(department1)

        if start_date and end_date:
            mask &= (df["start_date"] >= pd.to_datetime(start_date)) & (df["start_date"] <= pd.to_datetime(end_date))

        return df[mask]
    
    @cache.memoize()
    def get_filtered_dataframe_performance(dropdown_employee, department1_tuple, start_date, end_date):
        """Récupère et filtre les données avec mise en cache"""
        department1 = list(department1_tuple) if department1_tuple else None
        return filter_data_performance(employee_valid_rating, dropdown_employee,department1, start_date, end_date)


    
    @app.callback(
    [Output("pie_statut", "figure"),
     Output("pie_gender", "figure")],
    [Input('dropdown_country', "value"),
     Input("sexe", "value"),
     Input('department', 'value')],
    prevent_initial_call=False
)
    def pie_chart(dropdown_country=None, sexe=None, department=None):
    # Convertir les listes en tuples pour le caching
       sexe_tuple = tuple(sexe) if sexe else None
       department_tuple = tuple(department) if department else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
       filtered_call = get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple)
    
    # Calculer les agrégations pour les graphiques circulaires
       project_status = filtered_call['status'].value_counts().reset_index(name='count').rename(columns={'index': 'status'})
       project_gender = filtered_call['gender'].value_counts().reset_index(name='count').rename(columns={'index': 'gender'})
    
    # Créer les graphiques
       pie_status = create_pie_status(
       project_status, 'count', 'status',
        color_discrete_map={'to_do':'#8C1F1F','in_progress':'#285939','done':'#4B8C49'}
       )
       pie_gender = create_pie_status(
       project_gender, 'count', 'gender',
        color_discrete_map={'male':'#8C1F1F','female':'#285939'}
       )
    
       return pie_status, pie_gender

    @app.callback(
    [Output("bar_employee", "figure"),
     Output("bar_country", "figure")],
    [Input('dropdown_country', "value"),
     Input("sexe", "value"),
     Input('department', 'value')],
    prevent_initial_call=False
)
    def bar_chart(dropdown_country=None, sexe=None, department=None):
    # Convertir les listes en tuples pour le caching
       sexe_tuple = tuple(sexe) if sexe else None
       department_tuple = tuple(department) if department else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
       filtered_call = get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple)
    
    # Optimiser les groupby avec agg pour faire les calculs en une seule passe
       nb_ids_par_dept = filtered_call.groupby('department_id')['id_x'].nunique().reset_index().rename(columns={'id_x': 'nombre_employes'})
       nb_ids_par_country = filtered_call.groupby('country_id')['id_x'].nunique().reset_index().rename(columns={'id_x': 'nombre_employes'})
    
    # Créer les graphiques
       bar_employee = create_bar_chart(nb_ids_par_dept, 'department_id', 'nombre_employes')
       bar_country = create_bar_chart(nb_ids_par_country, 'country_id', 'nombre_employes')
    
       return bar_employee, bar_country

    @app.callback(
    [Output("kpi_employee", "children"),
     Output("kpi_homme", "children"),
     Output("kpi_femme", "children"),
     Output("kpi_projet", "children")],
    [Input('dropdown_country', "value"),
     Input("sexe", "value"),
     Input('department', 'value')],
    prevent_initial_call=False
    )
    def kpi_value(dropdown_country=None, sexe=None, department=None):
    # Convertir les listes en tuples pour le caching
        sexe_tuple = tuple(sexe) if sexe else None
        department_tuple = tuple(department) if department else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
        filtered_call = get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple)
    
    # Calculer les KPIs optimisés
        nb_employee = filtered_call['id_x'].nunique()
    
    # Créer un DataFrame agrégé par genre une seule fois pour éviter de refiltrer
        gender_counts = filtered_call.groupby('gender')['id_x'].nunique()
        nb_homme = gender_counts.get('male', 0)  
        nb_femme = gender_counts.get('female', 0)
    
        nb_projet = filtered_call['id_y'].nunique()
    
        return nb_employee, nb_homme, nb_femme, nb_projet
    
    ###########callbacks pour l'analyse des performances###################
    @app.callback(
    [Output("nbre_projet", "children"),
    Output("nbre_tache", "children"),
    Output("date_delai", "children"),
    ],
    [Input('dropdown_employee', "value"),
     Input('department1', 'value'),
     Input('date-input', 'value'),
     ],
    prevent_initial_call=False
    )
    def kpi_value(dropdown_employee=None, department1=None,date_range=None):
        start_date = None
        end_date = None

        if date_range and isinstance(date_range, list) and len(date_range) == 2:
           start_date = date_range[0]
           end_date = date_range[1]
           print(f"Date filtre: {start_date} à {end_date}")
        else:
           print(f"Date range invalide: {date_range}")
        
        department_tuple = tuple(department1) if department1 else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
        filtered_performance = get_filtered_dataframe_performance(dropdown_employee,department_tuple,start_date,end_date)
    
    # Calculer les KPIs optimisés
        nb_projet = filtered_performance['project'].nunique()
        nb_tache = filtered_performance['name_y'].nunique()
        date_delai_jours = (filtered_performance['expected_end_date'] - filtered_performance['end_date']).dt.days.fillna(0).astype(int)
        moyenne_delai = date_delai_jours.mean()
        moyenne_delai = 0 if math.isnan(moyenne_delai) else moyenne_delai
        jours = int(abs(moyenne_delai))
        heures = int((abs(moyenne_delai) - jours) * 24)
        color = "#285939" if moyenne_delai > 0 else "#8C1F1F" if moyenne_delai < 0 else "#8C1F1F"

        # Déterminer le texte explicatif
        delai_text = "(avant délai)" if moyenne_delai > 0 else "(après délai)" if moyenne_delai < 0 else ""

        # Formattage HTML stylisé dans un seul conteneur
        moyenne_formattee = html.Div([
        html.Span(f"{jours} j {heures} h", style={"color": color, "fontSize": "2em", "fontWeight": "bold", "display": "block"}),
        html.Span(delai_text, style={"color": color, "fontSize": "0.7em",'fontWeight':'bold',"display": "block", "marginTop": "-3px"})
        ], className="text-center")
        return nb_projet,nb_tache,moyenne_formattee
    

    @app.callback(
    [Output("taux_satisfaction", "figure"),
    Output("taux_task", "figure"), ],
    [Input('dropdown_employee', "value"),
     Input('department1', 'value'),
     Input('date-input', 'value'),
     ],
    prevent_initial_call=False
    )
    def kpi_value(dropdown_employee=None, department1=None,date_range=None):
        start_date = None
        end_date = None

        if date_range and isinstance(date_range, list) and len(date_range) == 2:
           start_date = date_range[0]
           end_date = date_range[1]
           print(f"Date filtre: {start_date} à {end_date}")
        else:
           print(f"Date range invalide: {date_range}")
        
        department_tuple = tuple(department1) if department1 else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
        filtered_performance = get_filtered_dataframe_performance(dropdown_employee,department_tuple,start_date,end_date)
    
    # Calculer les KPIs optimisés
        taux_satisfaction=filtered_performance['rating'].mean()
        print(taux_satisfaction)

        gauge_satisfaction = create_gauge_chart(value=taux_satisfaction)
        employee_task = filtered_performance.dropna(subset=['status'])
        proportion_done = ((employee_task['status'] == 'Terminée').mean())*100
        gauge_task=create_gauge_task(value1=proportion_done)

        return gauge_satisfaction,gauge_task
    
    @app.callback(
    Output("datatable", "data"),
    [Input('dropdown_employee', "value"),
     Input('department1', 'value'),
     Input('date-input', 'value'),
     ],
    prevent_initial_call=False
    )
    def task_data(dropdown_employee=None, department1=None,date_range=None):
        start_date = None
        end_date = None

        if date_range and isinstance(date_range, list) and len(date_range) == 2:
           start_date = date_range[0]
           end_date = date_range[1]
           print(f"Date filtre: {start_date} à {end_date}")
        else:
           print(f"Date range invalide: {date_range}")
        
        department_tuple = tuple(department1) if department1 else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
        filtered_performance = get_filtered_dataframe_performance(dropdown_employee,department_tuple,start_date,end_date)
    
        result=filtered_performance[['name_x','name_y','manager_x','status','progress','rating','comments']]
        result.columns = ['employee', 'tache', 'manager', 'statut', 'progression', 'note', 'comments']
        result = result.reset_index()
        print(result)
        return result.to_dict('records')

    return app


# Démarrage de l'application
if __name__ == '__main__':
    app = create_dash_app()
    app.run(debug=False, host='127.0.0.1', port=8050, dev_tools_ui=True)
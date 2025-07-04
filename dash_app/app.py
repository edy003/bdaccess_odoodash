
import sys
print("Python utilisé :", sys.executable)
import dash
from dash import html, dcc, Input, Output, State
import logging
import math
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import requests
from flask_caching import Cache
# from widget import burger_component, create_pie_status, create_bar_chart, create_gauge_chart, create_gauge_task
import flask
from flask import request
import json
from pages import Analyse_globale , Performances ,Suivi,analyse
from widget import create_dropdown,generate_chip_selector,create_pie_status,create_bar_chart,get_date_range_component,create_gauge_chart,create_gauge_task

# Configuration du logging pour voir les messages dans le terminal
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_logger = logging.getLogger(__name__)


# # Configuration Odoo
# ODOO_BASE_URL = "http://localhost:8069"  # Remplacez par l'URL de votre serveur Odoo
# API_ENDPOINT = f"{ODOO_BASE_URL}/api/get_employee_data"
# AUTH_ENDPOINT = f"{ODOO_BASE_URL}/api/auth/login"

# Variables pour stocker les informations d'authentification
JWT_TOKEN = None
USER_INFO = None

def create_dash_app():    
    """Créer et configurer l'application Dash"""
    print("Création de l'application Dash...")
    app = dash.Dash(
        __name__,  # Double underscore correct
        requests_pathname_prefix='/dash/',  # Corrige les erreurs de chemin derrière Nginx
        routes_pathname_prefix='/dash/',    # Corrige le loading infini
        # assets_url_path='/dash/assets',
        use_pages=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.DATES],
        suppress_callback_exceptions=True    # Corrige le chargement des fichiers statiques
    )
    
    # Configuration du cache
    cache = Cache()
    cache.init_app(app.server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': './cache-directory',
        'CACHE_DEFAULT_TIMEOUT': 300
    })

    @cache.memoize(timeout=300)
    def fetch_api_data(token, endpoint_name, url):
        """Fonction cachée pour récupérer les données d'un endpoint"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return {"error": f"Erreur HTTP {response.status_code}"}
            
            if not response.text.strip():
                return []
            
            try:
                data = response.json()
                return data if not (isinstance(data, dict) and 'error' in data) else data
            except json.JSONDecodeError as e:
                return {"error": f"JSON invalide: {str(e)}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Erreur réseau: {str(e)}"}
        except Exception as e:
            return {"error": f"Erreur: {str(e)}"}

    @cache.memoize(timeout=600)  # Cache plus long pour les DataFrames
    def create_merged_dataframe(employees_data, projects_data):
        """Crée et cache le DataFrame fusionné"""
        try:
            if not isinstance(employees_data, list) or not isinstance(projects_data, list):
                return None
            
            if not employees_data or not projects_data:
                return None
                
            employee_df = pd.DataFrame(employees_data)
            projects_df = pd.DataFrame(projects_data)
            
            if 'department_id' not in employee_df.columns or 'department_id' not in projects_df.columns:
                return None
            
            merged = employee_df.merge(projects_df, on='department_id', how='outer')
            filtered = merged[merged['employee_id'].notna()].copy()
            return filtered.drop_duplicates(subset=['employee_id', 'project_id'])
            
        except Exception:
            return None
        
    @cache.memoize(timeout=600)  # Cache plus long pour les DataFrames
    def create_merged_performance_dataframe(employees_data, projects_data,tasks_data,ratings_data):
        """Crée et cache le DataFrame fusionné"""
        try:
        # Vérification des entrées
            for data in [employees_data, tasks_data, projects_data, ratings_data]:
                if not isinstance(data, list) or not data:
                    return None
                
            employees_df = pd.DataFrame(employees_data)
            tasks_df = pd.DataFrame(tasks_data)
            projects_df = pd.DataFrame(projects_data)
            ratings_df = pd.DataFrame(ratings_data)
            
            employee_task = employees_df.merge(tasks_df, left_on='employee_id', right_on='employee_task', how='outer')
            employee_task_project = employee_task.merge(projects_df, left_on='project_task', right_on='project_id', how='outer')
            employee_task_rating = employee_task_project.merge(ratings_df, left_on='employee_id', right_on='employee_rate', how='outer')
            employee_valid_rating = employee_task_rating[employee_task_rating['employee_id'].notna()].copy()
            employee_valid_rating['expected_end_date']=pd.to_datetime(employee_valid_rating['expected_end_date'])
            employee_valid_rating['start_date_x']=pd.to_datetime(employee_valid_rating['start_date_x'])
            employee_valid_rating['end_date_x']=pd.to_datetime(employee_valid_rating['end_date_x'])
            # employee_valid_rating = employee_valid_rating[employee_valid_rating['start_date_x'].notna()]
            return employee_valid_rating
            
        except Exception:
            return None
        
    @cache.memoize(timeout=600)  # Cache plus long pour les DataFrames
    def create_merged_suivi_dataframe(employees_data, projects_data,tasks_data,subtasks_data):
        """Crée et cache le DataFrame fusionné"""
        try:
        # Vérification des entrées
            for data in [employees_data, tasks_data, projects_data, subtasks_data]:
                if not isinstance(data, list) or not data:
                    return None
                
            employees_df = pd.DataFrame(employees_data)
            tasks_df = pd.DataFrame(tasks_data)
            projects_df = pd.DataFrame(projects_data)
            subtasks_df = pd.DataFrame(subtasks_data)
            employee_task = employees_df.merge(tasks_df,left_on='employee_id',right_on='employee_task',how='outer')
            employee_suivi = employee_task.merge(subtasks_df,left_on='tache_id',right_on='task',how='outer')
            employee_suivi = employee_suivi.merge(projects_df,left_on='project_task',right_on='project_id',how='outer')
            employee_suivi = employee_suivi[employee_suivi['employee_id'].notna()].copy()
            employee_suivi['start_date_x']=pd.to_datetime(employee_suivi['start_date_x'])
            employee_suivi['expected_end_date']=pd.to_datetime(employee_suivi['expected_end_date'])
            employee_suivi['end_date_x']=pd.to_datetime(employee_suivi['end_date_x'])

            return employee_suivi
            
        except Exception:
            return None
    

    def extract_data_list(data_obj):
        """Extrait la liste de données depuis l'objet Odoo"""
        if isinstance(data_obj, list):
            return data_obj
        if isinstance(data_obj, dict) and not data_obj.get('error'):
            for key, value in data_obj.items():
                if isinstance(value, list):
                    return value
        return data_obj
    
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
    
    
    def filter_data_performance(df, dropdown_employee=None, department1=None, start_date=None, end_date=None):

        mask = pd.Series(True, index=df.index)

        if dropdown_employee:
            mask &= (df['employee_name'] == dropdown_employee)

        if department1:
            mask &= (df["department_id_y"].isin(department1))

        if start_date and end_date:
            mask &= (df["start_date_x"] >= pd.to_datetime(start_date)) & (df["start_date_x"] <= pd.to_datetime(end_date))

        return df[mask]

    def login_layout():
        return html.Div([
            html.Div([
                dmc.MantineProvider(
                    theme={"colorScheme": "light"},
                    children=[
                        dmc.Stack([
                            dmc.TextInput(
                                placeholder="Your login",
                                id='login-input'
                            ),
                            dmc.PasswordInput(
                                placeholder="Your password",
                                id='password-input'
                            ),
                            dmc.Button(
                                "Se connecter",
                                id='login-button', 
                                n_clicks=0,
                                style={"backgroundColor": "#43a047"}
                            ),
                            html.Div(id='login-feedback')  # Pour afficher les erreurs
                        ])
                    ]
                ),
            ], style={"width": "360px", "padding": "45px", "backgroundColor": "#FFFFFF"}),
        ], style={
            'minHeight': '100vh',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'backgroundColor': '#76b852'
        })
    
    # Définir la mise en page de base
    app.layout = html.Div([
    dcc.Store(id='jwt-token'),  # Stocker le token ici
    dcc.Store(id='all-data'),
    dcc.Store(id='suivi-data'),
    dcc.Store(id='performance-data'),
    dcc.Store(id="user-info"),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=login_layout())]
    )
    
    # Définir les callbacks
    @app.callback(
    Output('jwt-token', 'data'),
    Output('user-info', 'data'),
    # Output('url', 'pathname'), 
    # Output('login-feedback', 'children'),
    Input('login-button', 'n_clicks'),
    State('login-input', 'value'),
    State('password-input', 'value'),
    prevent_initial_call=True
)
    def login(n_clicks, login, password):
        if not login or not password:
            return None, "Veuillez saisir votre login et mot de passe"
        
        try:
            # Envoyer la requête au format attendu par l'API
            res = requests.post(
                "http://localhost:8069/api/auth/login", 
                json={"login": login, "password": password},
                timeout=10
            )
            
            print(f"Code de statut: {res.status_code}")
            print(f"Réponse brute: {res.text}")
            
            # Récupérer le résultat
            data = res.json()
            
            # Structure attendue basée sur votre code fonctionnel
            result = data.get("result", data)  # Essaie d'obtenir 'result' sinon utilise la réponse entière
            
            print(f"Données de résultat: {result}")
            
            # Vérifier le succès
            if not result or not result.get("success"):
                error_msg = result.get("error") if result and result.get("error") else "Erreur inconnue du serveur"
                return None, f"Erreur: {error_msg}"
            
            # Si la connexion réussit
            token = result.get("token")
            user_info = result.get("user", {})
            # if user_info.get("role") == "admin":
            #     target_page = "/admin"
            # else:
            #     target_page = "/employee"
            
            
            return token,user_info
            
        except Exception as e:
            import traceback
            print(f"Exception détaillée: {traceback.format_exc()}")
            return None, f"Erreur inattendue: {str(e)}"
    
    @app.callback(
    Output('page-content', 'children'),
    Input("user-info", "data"),
    prevent_initial_call=True
    )
    def redirect_based_on_role(user_info,):
        if not user_info:
            return login_layout
        role = user_info.get("role")
        if role == "admin":
            return Analyse_globale.layout
        elif role == "employee":
            return Performances.layout
        return login_layout

        
    # @app.callback(
    # Output('employee-data', 'data'),
    # Input('jwt-token', 'data'),
    # prevent_initial_call=True
    # )
    # def fetch_employee_data(token):
    #     if not token:
    #         return "Vous devez vous connecter pour voir les données."
    
    #     try:
    #         headers = {
    #         'Authorization': f'Bearer {token}',
    #     }
        
    #     # Ajouter des logs pour le débogage
    #         print(f"Envoi de requête avec token: {token[:10]}...")
        
    #         response = requests.get(
    #         "http://localhost:8069/api/get_employee_ratings",
    #         headers=headers
    #     )
        
    #     # Afficher la réponse brute
    #         print(f"Code de statut: {response.status_code}")
    #         print(f"Headers: {response.headers}")
    #         print(f"Contenu brut: {response.text}")
        
    #     # Vérifier si la réponse est vide
    #         if not response.text:
    #             return "Erreur: La réponse du serveur est vide"
        
    #     # Vérifier si la réponse est du JSON valide avant de la parser
    #         try:
    #             data = response.json()
    #             print("data:",data)
    #             return data
    #         except json.JSONDecodeError as e:
    #             return f"Erreur: Impossible de décoder la réponse JSON: {str(e)}, Contenu: {response.text[:100]}"
            
    #     except Exception as e:
    #         import traceback
    #         print(f"Exception détaillée: {traceback.format_exc()}")
    #         return f"Erreur lors de la récupération des données: {str(e)}"
        

    @app.callback(    
    Output('all-data', 'data'),
    Input('jwt-token', 'data'),
    prevent_initial_call=True
)
    def fetch_all_data(token):
        if not token:
            return {"error": "Vous devez vous connecter pour voir les données."}
        
        try:
            endpoints = {
                'employees': "http://localhost:8069/api/get_employee_data",
                'projects': "http://localhost:8069/api/get_projects",
            }
            
            all_data = {}
            
            # Utiliser la fonction cachée pour chaque endpoint
            for key, url in endpoints.items():
                all_data[key] = fetch_api_data(token, key, url)
            
            return all_data
            
        except Exception as e:
            return {"error": str(e)}
        
    @app.callback(    
    Output('performance-data', 'data'),
    Input('jwt-token', 'data'),
    prevent_initial_call=True
)
    def fetch_performance_data(token):
        if not token:
            return {"error": "Vous devez vous connecter pour voir les données."}
        
        try:
            endpoints = {
                'employees': "http://localhost:8069/api/get_employee_data",
                'projects': "http://localhost:8069/api/get_projects",
                'tasks': "http://localhost:8069/api/get_tasks",
                'ratings': "http://localhost:8069/api/get_employee_ratings",
            }
            
            performance_data = {}
            
            # Utiliser la fonction cachée pour chaque endpoint
            for key, url in endpoints.items():
                performance_data[key] = fetch_api_data(token, key, url)

            return performance_data
            
        except Exception as e:
            return {"error": str(e)}
        
    
    @app.callback(    
    Output('suivi-data', 'data'),
    Input('jwt-token', 'data'),
    prevent_initial_call=True
)
    def fetch_performance_data(token):
        if not token:
            return {"error": "Vous devez vous connecter pour voir les données."}
        
        try:
            endpoints = {
                'employees': "http://localhost:8069/api/get_employee_data",
                'projects': "http://localhost:8069/api/get_projects",
                'tasks': "http://localhost:8069/api/get_tasks",
                'subtasks':"http://localhost:8069/api/get_subtasks",
            }
            
            suivi_data = {}
            
            # Utiliser la fonction cachée pour chaque endpoint
            for key, url in endpoints.items():
                suivi_data[key] = fetch_api_data(token, key, url)

            return suivi_data
            
        except Exception as e:
            return {"error": str(e)}
        
        
    @app.callback(
    Output('dropdown_country', 'children'),
    Output('sexe', 'children'),
    Output('department', 'children'),
    Input('all-data', 'data'),
    #  Input('url1', 'pathname'),
    prevent_initial_call=False
)
    def process_employees_and_projects(all_data):
        # if pathname != '/':
        #     return dash.no_update,dash.no_update,dash.no_update

        if not all_data or (isinstance(all_data, dict) and 'error' in all_data and len(all_data) == 1):    
            return f"Erreur: {all_data.get('error', 'Données manquantes')}"
        
        # Extraction des données
        employees_raw = all_data.get('employees', {})
        projects_raw = all_data.get('projects', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        
        # Vérifications d'erreur
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):    
            return "Erreurs détectées dans les données"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):    
            return "Aucune donnée disponible"
        
        try:
            # Utiliser la fonction cachée pour créer le DataFrame
            employee_project_valid = create_merged_dataframe(employees, projects)
            
            if employee_project_valid is None or employee_project_valid.empty:
                return "Erreur: Impossible de fusionner les données"
            
            if 'country_id' not in employee_project_valid.columns:
                return "Erreur: Colonne 'country_id' manquante"
            
            unique_countries = employee_project_valid['country_id'].unique()
            option_gender = employee_project_valid['gender'].unique()
            option_department = employee_project_valid['department_id'].unique()
            
            return create_dropdown(label="Country",options=unique_countries,dropdown_id='dropdown_country'),generate_chip_selector(
                 id="sexe",label="Sexe",options=option_gender,multiple=True
            ),generate_chip_selector(id="department",label="Department",options=option_department,multiple=True)
            
        except Exception as e:
            return f"Erreur de traitement: {str(e)}"
        
    
    @app.callback(
     [Output("pie_statut", "figure"),
     Output("pie_gender", "figure")],
    [Input('all-data', 'data'),
     Input('dropdown_country', "value"),
     Input("sexe", "value"),
     Input('department', 'value')],
    prevent_initial_call=True
)
    def piechart(all_data,dropdown_country=None, sexe=None, department=None):
        if not all_data or (isinstance(all_data, dict) and 'error' in all_data and len(all_data) == 1):    
            return f"Erreur: {all_data.get('error', 'Données manquantes')}"
        
        # Extraction des données
        employees_raw = all_data.get('employees', {})
        projects_raw = all_data.get('projects', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        
        # Vérifications d'erreur
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):    
            return "Erreurs détectées dans les données"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):    
            return "Aucune donnée disponible"
        
        try:
            # Utiliser la fonction cachée pour créer le DataFrame
            employee_project_valid = create_merged_dataframe(employees, projects)

            @cache.memoize()
            def get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple):
                """Récupère et filtre les données avec mise en cache"""
                 # Convertir les tuples en listes pour le filtrage
                sexe = list(sexe_tuple) if sexe_tuple else None
                department = list(department_tuple) if department_tuple else None
                return filter_data(employee_project_valid, dropdown_country, sexe, department)
            
            if employee_project_valid is None or employee_project_valid.empty:
                return "Erreur: Impossible de fusionner les données"
            
            if 'country_id' not in employee_project_valid.columns:
                return "Erreur: Colonne 'country_id' manquante"
            
            sexe_tuple = tuple(sexe) if sexe else None
            department_tuple = tuple(department) if department else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
            filtered_call = get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple)
    
   
       # Ceci comptera le nombre de projets uniques par statut
            project_status = filtered_call.groupby('status')['project_id'].nunique().reset_index(name='count')
       # Ceci comptera le nombre de projets uniques par statut
            project_gender = filtered_call.groupby('gender')['employee_id'].nunique().reset_index(name='count')
            
    
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
        
            
        except Exception as e:
            return f"Erreur de traitement: {str(e)}"
        
    @app.callback(
    [Output("bar_employee", "figure"),
   Output("bar_country", "figure")],
    [Input('all-data', 'data'),
     Input('dropdown_country', "value"),
     Input("sexe", "value"),
     Input('department', 'value')],
    prevent_initial_call=True
)
    def piechart(all_data,dropdown_country=None, sexe=None, department=None):
        if not all_data or (isinstance(all_data, dict) and 'error' in all_data and len(all_data) == 1):    
            return f"Erreur: {all_data.get('error', 'Données manquantes')}"
        
        # Extraction des données
        employees_raw = all_data.get('employees', {})
        projects_raw = all_data.get('projects', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        
        # Vérifications d'erreur
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):    
            return "Erreurs détectées dans les données"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):    
            return "Aucune donnée disponible"
        
        try:
            # Utiliser la fonction cachée pour créer le DataFrame
            employee_project_valid = create_merged_dataframe(employees, projects)

            @cache.memoize()
            def get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple):
                """Récupère et filtre les données avec mise en cache"""
                 # Convertir les tuples en listes pour le filtrage
                sexe = list(sexe_tuple) if sexe_tuple else None
                department = list(department_tuple) if department_tuple else None
                return filter_data(employee_project_valid, dropdown_country, sexe, department)
            
            if employee_project_valid is None or employee_project_valid.empty:
                return "Erreur: Impossible de fusionner les données"
            
            if 'country_id' not in employee_project_valid.columns:
                return "Erreur: Colonne 'country_id' manquante"
            
            sexe_tuple = tuple(sexe) if sexe else None
            department_tuple = tuple(department) if department else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
            filtered_call = get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple)
    
    # Optimiser les groupby avec agg pour faire les calculs en une seule passe
            nb_ids_par_dept = filtered_call.groupby('department_id')['employee_id'].nunique().reset_index().rename(columns={'employee_id': 'nombre_employes'})
            nb_ids_par_country = filtered_call.groupby('country_id')['employee_id'].nunique().reset_index().rename(columns={'employee_id': 'nombre_employes'})
    
    # Créer les graphiques
            bar_employee = create_bar_chart(nb_ids_par_dept, 'department_id', 'nombre_employes')
            bar_country = create_bar_chart(nb_ids_par_country, 'country_id', 'nombre_employes')
    
            return bar_employee, bar_country
            
        except Exception as e:
            return f"Erreur de traitement: {str(e)}"
        

    @app.callback(
     [Output("kpi_employee", "children"),
     Output("kpi_homme", "children"),
     Output("kpi_femme", "children"),
     Output("kpi_projet", "children")],
    [Input('all-data', 'data'),
     Input('dropdown_country', "value"),
     Input("sexe", "value"),
     Input('department', 'value')],
    prevent_initial_call=True
)
    def piechart(all_data,dropdown_country=None, sexe=None, department=None):
        if not all_data or (isinstance(all_data, dict) and 'error' in all_data and len(all_data) == 1):    
            return f"Erreur: {all_data.get('error', 'Données manquantes')}"
        
        # Extraction des données
        employees_raw = all_data.get('employees', {})
        projects_raw = all_data.get('projects', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        
        
        # Vérifications d'erreur
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):    
            return "Erreurs détectées dans les données"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):    
            return "Aucune donnée disponible"
        
        try:
            # Utiliser la fonction cachée pour créer le DataFrame
            employee_project_valid = create_merged_dataframe(employees, projects)

            @cache.memoize()
            def get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple):
                """Récupère et filtre les données avec mise en cache"""
                 # Convertir les tuples en listes pour le filtrage
                sexe = list(sexe_tuple) if sexe_tuple else None
                department = list(department_tuple) if department_tuple else None
                return filter_data(employee_project_valid, dropdown_country, sexe, department)
            
            # if employee_project_valid is None or employee_project_valid.empty:
            #     return "Erreur: Impossible de fusionner les données"
            
            # if 'country_id' not in employee_project_valid.columns:
            #     return "Erreur: Colonne 'country_id' manquante"
            
            sexe_tuple = tuple(sexe) if sexe else None
            department_tuple = tuple(department) if department else None
    
    # Utiliser la fonction en cache pour obtenir les données filtrées
            filtered_call = get_filtered_dataframe(dropdown_country, sexe_tuple, department_tuple)
            nb_employee = filtered_call['employee_id'].nunique()
    
    # Créer un DataFrame agrégé par genre une seule fois pour éviter de refiltrer
            gender_counts = filtered_call.groupby('gender')['employee_id'].nunique()
            nb_homme = gender_counts.get('male', 0)  
            nb_femme = gender_counts.get('female', 0)
    
            nb_projet = filtered_call['project_id'].nunique()
    
            return nb_employee, nb_homme, nb_femme, nb_projet
    
            
            
        except Exception as e:
            return f"Erreur de traitement: {str(e)}"
        
    
    #performances callback
    @app.callback(
    Output('dropdown_employee', 'children'),
    Output('department1', 'children'),
    Output('date-input', 'children'),
    Input('performance-data', 'data'),
    prevent_initial_call=False
)
    def process_performance_data(performance_data):
        # print(f"Type de performance_data : {type(performance_data)}")
        # print(f"Contenu de performance_data : {performance_data}")

        # Cas d'erreur dès le départ
        if not performance_data or (isinstance(performance_data, dict) and 'error' in performance_data and len(performance_data) == 1):
            error_msg = f"Erreur: {performance_data.get('error', 'Données manquantes')}"
            return error_msg, error_msg, error_msg
        
        # Extraction des données
        employees_raw = performance_data.get('employees', {})
        projects_raw = performance_data.get('projects', {})
        tasks_raw = performance_data.get('tasks', {})
        ratings_raw = performance_data.get('ratings', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        tasks = extract_data_list(tasks_raw)
        ratings = extract_data_list(ratings_raw)
        
        
        # Vérification des erreurs de format
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):
            return "Erreur: Données corrompues", "Erreur: Données corrompues", "Erreur: Données corrompues"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):
            return "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible"
        
        try:
            # Fusion des données
            employee_valid_rating = create_merged_performance_dataframe(employees, projects, tasks, ratings)
            # print(employee_valid_rating.columns)
            
            if employee_valid_rating is None or employee_valid_rating.empty:
                error_msg = "Erreur: Impossible de fusionner les données"
                return error_msg, error_msg, error_msg
            
            # Préparation des composants
            option_department = employee_valid_rating['department_id_y'].dropna().unique()
            option_employee_name = employee_valid_rating['employee_name'].unique()
            date_min = employee_valid_rating['start_date_x'].min()
            date_max = employee_valid_rating['start_date_x'].max()
            print(option_employee_name)
            
            return (
                create_dropdown(label="Employee", options=option_employee_name, dropdown_id='dropdown_employee'),
                generate_chip_selector(id="department1", label="Department", options=option_department, multiple=True),
                get_date_range_component(date_min, date_max, id="date-input")
            )
        
        except Exception as e:
            error_msg = f"Erreur de traitement: {str(e)}"
            return error_msg, error_msg, error_msg
    
    @app.callback(
    [Output("taux_satisfaction", "figure"),
    Output("taux_task", "figure"), ],
    [
    Input('performance-data', 'data'),
    Input('dropdown_employee', "value"),
    Input('department1', 'value'),
    Input('date-input', 'value'),
    ],
    prevent_initial_call=False
    )
    def gauge_value(performance_data,dropdown_employee=None, department1=None, date_range=None):
        # Cas d'erreur dès le départ
        if not performance_data or (isinstance(performance_data, dict) and 'error' in performance_data and len(performance_data) == 1):
            error_msg = f"Erreur: {performance_data.get('error', 'Données manquantes')}"
            return error_msg, error_msg, error_msg
        
        # Extraction des données
        employees_raw = performance_data.get('employees', {})
        projects_raw = performance_data.get('projects', {})
        tasks_raw = performance_data.get('tasks', {})
        ratings_raw = performance_data.get('ratings', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        tasks = extract_data_list(tasks_raw)
        ratings = extract_data_list(ratings_raw)
        
        
        # Vérification des erreurs de format
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):
            return "Erreur: Données corrompues", "Erreur: Données corrompues", "Erreur: Données corrompues"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):
            return "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible"
        
        try:
            # Fusion des données
            employee_valid_rating = create_merged_performance_dataframe(employees, projects, tasks, ratings)
            
            if employee_valid_rating is None or employee_valid_rating.empty:
                error_msg = "Erreur: Impossible de fusionner les données"
                return error_msg, error_msg, error_msg
            
            @cache.memoize()
            def get_filtered_dataframe_performance(dropdown_employee, department1_tuple, start_date, end_date):
                """Récupère et filtre les données avec mise en cache"""
                department1 = list(department1_tuple) if department1_tuple else None
                return filter_data_performance(employee_valid_rating, dropdown_employee,department1, start_date, end_date)

            start_date = None
            end_date = None
            if date_range and isinstance(date_range, list) and len(date_range) == 2:
                start_date = date_range[0]
                end_date = date_range[1]
            #     print(f"Date filtre: {start_date} à {end_date}")
            # else:
            #     print(f"Date range invalide: {date_range}")
        
            department1 = list(department1) if department1 else None
            filtered_performance = get_filtered_dataframe_performance(dropdown_employee, department1,start_date,end_date)
            taux_satisfaction=filtered_performance['rating'].mean()
            gauge_satisfaction = create_gauge_chart(value=taux_satisfaction)
            employee_task = filtered_performance.dropna(subset=['status_x'])
            proportion_done = ((employee_task['status_x'] == 'Terminée').mean())*100
            gauge_task=create_gauge_task(value1=proportion_done)

            return gauge_satisfaction,gauge_task    
        except Exception as e:
            error_msg = f"Erreur de traitement: {str(e)}"
            return error_msg, error_msg, error_msg
        

    @app.callback(
    [Output("nbre_projet", "children"),
    Output("nbre_tache", "children"),
    Output("date_delai", "children") ],
    [
    Input('performance-data', 'data'),
    Input('dropdown_employee', "value"),
    Input('department1', 'value'),
    Input('date-input', 'value'),
    ],
    prevent_initial_call=False
    )
    def gauge_value(performance_data,dropdown_employee=None, department1=None, date_range=None):
        # Cas d'erreur dès le départ
        if not performance_data or (isinstance(performance_data, dict) and 'error' in performance_data and len(performance_data) == 1):
            error_msg = f"Erreur: {performance_data.get('error', 'Données manquantes')}"
            return error_msg, error_msg, error_msg
        
        # Extraction des données
        employees_raw = performance_data.get('employees', {})
        projects_raw = performance_data.get('projects', {})
        tasks_raw = performance_data.get('tasks', {})
        ratings_raw = performance_data.get('ratings', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        tasks = extract_data_list(tasks_raw)
        ratings = extract_data_list(ratings_raw)
        
        
        # Vérification des erreurs de format
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):
            return "Erreur: Données corrompues", "Erreur: Données corrompues", "Erreur: Données corrompues"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):
            return "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible"
        
        try:
            # Fusion des données
            employee_valid_rating = create_merged_performance_dataframe(employees, projects, tasks, ratings)
            
            if employee_valid_rating is None or employee_valid_rating.empty:
                error_msg = "Erreur: Impossible de fusionner les données"
                return error_msg, error_msg, error_msg
            
            @cache.memoize()
            def get_filtered_dataframe_performance(dropdown_employee, department1_tuple, start_date, end_date):
                """Récupère et filtre les données avec mise en cache"""
                department1 = list(department1_tuple) if department1_tuple else None
                return filter_data_performance(employee_valid_rating, dropdown_employee,department1, start_date, end_date)

            start_date = None
            end_date = None
            if date_range and isinstance(date_range, list) and len(date_range) == 2:
                start_date = date_range[0]
                end_date = date_range[1]
                print(f"Date filtre: {start_date} à {end_date}")
            else:
                print(f"Date range invalide: {date_range}")
        
            department1 = list(department1) if department1 else None
            filtered_performance = get_filtered_dataframe_performance(dropdown_employee, department1,start_date,end_date)
            nb_projet = filtered_performance['project_id'].nunique()
            nb_tache = filtered_performance['tache_id'].nunique()
            date_delai_jours = (filtered_performance['expected_end_date'] - filtered_performance['end_date_x']).dt.days.fillna(0).astype(int)
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
        except Exception as e:
            error_msg = f"Erreur de traitement: {str(e)}"
            return error_msg, error_msg, error_msg
    

    @app.callback(
    Output("employee_name", "children"),
    Output("employee_department", "children"),
    [
    Input('performance-data', 'data'),
    Input('dropdown_employee', "value"),
    ],
    prevent_initial_call=False
    )
    def gauge_value(performance_data,dropdown_employee=None, department1=None, date_range=None):
        # Cas d'erreur dès le départ
        if not performance_data or (isinstance(performance_data, dict) and 'error' in performance_data and len(performance_data) == 1):
            error_msg = f"Erreur: {performance_data.get('error', 'Données manquantes')}"
            return error_msg, error_msg, error_msg
        
        # Extraction des données
        employees_raw = performance_data.get('employees', {})
        projects_raw = performance_data.get('projects', {})
        tasks_raw = performance_data.get('tasks', {})
        ratings_raw = performance_data.get('ratings', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        tasks = extract_data_list(tasks_raw)
        ratings = extract_data_list(ratings_raw)
        
        
        # Vérification des erreurs de format
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):
            return "Erreur: Données corrompues", "Erreur: Données corrompues", "Erreur: Données corrompues"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):
            return "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible"
        
        try:
            # Fusion des données
            employee_valid_rating = create_merged_performance_dataframe(employees, projects, tasks, ratings)
            
            if employee_valid_rating is None or employee_valid_rating.empty:
                error_msg = "Erreur: Impossible de fusionner les données"
                return error_msg, error_msg, error_msg
            
            @cache.memoize()
            def get_filtered_dataframe_performance(dropdown_employee, department1_tuple, start_date, end_date):
                """Récupère et filtre les données avec mise en cache"""
                department1 = list(department1_tuple) if department1_tuple else None
                return filter_data_performance(employee_valid_rating, dropdown_employee,department1, start_date, end_date)

            start_date = None
            end_date = None
            if date_range and isinstance(date_range, list) and len(date_range) == 2:
                start_date = date_range[0]
                end_date = date_range[1]
                print(f"Date filtre: {start_date} à {end_date}")
            else:
                print(f"Date range invalide: {date_range}")

            if not dropdown_employee:
                return "QC_EMPLOYEE", "QC_DEPARTMENT"
        
            department1 = list(department1) if department1 else None
            filtered_performance = get_filtered_dataframe_performance(dropdown_employee, department1,start_date,end_date)
            employee_name=filtered_performance['employee_name'].unique()
            employee_department=filtered_performance['department_id_x'].unique()
        
            return employee_name,employee_department 
        except Exception as e:
            error_msg = f"Erreur de traitement: {str(e)}"
            return error_msg, error_msg, error_msg


    @app.callback(
    Output("column-groups-note", "rowData"),
    [
    Input('performance-data', 'data'),
    Input('dropdown_employee', "value"),
    Input('department1', 'value'),
    Input('date-input', 'value'),
    ],
    prevent_initial_call=False
    )
    def table_value(performance_data,dropdown_employee=None, department1=None, date_range=None):
        # Cas d'erreur dès le départ
        if not performance_data or (isinstance(performance_data, dict) and 'error' in performance_data and len(performance_data) == 1):
            error_msg = f"Erreur: {performance_data.get('error', 'Données manquantes')}"
            return error_msg, error_msg, error_msg
        
        # Extraction des données
        employees_raw = performance_data.get('employees', {})
        projects_raw = performance_data.get('projects', {})
        tasks_raw = performance_data.get('tasks', {})
        ratings_raw = performance_data.get('ratings', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        tasks = extract_data_list(tasks_raw)
        ratings = extract_data_list(ratings_raw)
        
        
        # Vérification des erreurs de format
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):
            return "Erreur: Données corrompues", "Erreur: Données corrompues", "Erreur: Données corrompues"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):
            return "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible"
        
        try:
            # Fusion des données
            employee_valid_rating = create_merged_performance_dataframe(employees, projects, tasks, ratings)
            
            if employee_valid_rating is None or employee_valid_rating.empty:
                error_msg = "Erreur: Impossible de fusionner les données"
                return error_msg, error_msg, error_msg
            
            @cache.memoize()
            def get_filtered_dataframe_performance(dropdown_employee, department1_tuple, start_date, end_date):
                """Récupère et filtre les données avec mise en cache"""
                department1 = list(department1_tuple) if department1_tuple else None
                return filter_data_performance(employee_valid_rating, dropdown_employee,department1, start_date, end_date)

            start_date = None
            end_date = None
            if date_range and isinstance(date_range, list) and len(date_range) == 2:
                start_date = date_range[0]
                end_date = date_range[1]
                print(f"Date filtre: {start_date} à {end_date}")
            else:
                print(f"Date range invalide: {date_range}")
        
            department1 = list(department1) if department1 else None
            filtered_performance = get_filtered_dataframe_performance(dropdown_employee, department1,start_date,end_date)
            result=filtered_performance[['employee_name','project_name','tache_name_x','employee_project','rating','comments']]
            result.columns = ['Employee','Projet','Tache', 'Manager', 'Note', 'Commentaire']
            result = result.reset_index(drop=True) 
            return result.to_dict('records') 
        except Exception as e:
            error_msg = f"Erreur de traitement: {str(e)}"
            return error_msg
        
    #suivi callback

    @app.callback(
    Output('dropdown_employee2', 'children'),
    Output('department2', 'children'),
    Output('date-input2', 'children'),
    Input('suivi-data', 'data'),
    prevent_initial_call=False
)
    def process_performance_data(suivi_data):
        # print(f"Type de suivi_data : {type(suivi_data)}")
        # print(f"Contenu de suivi_data : {suivi_data}")

        # Cas d'erreur dès le départ
        if not suivi_data or (isinstance(suivi_data, dict) and 'error' in suivi_data and len(suivi_data) == 1):
            error_msg = f"Erreur: {suivi_data.get('error', 'Données manquantes')}"
            return error_msg, error_msg, error_msg
        
        # Extraction des données
        employees_raw = suivi_data.get('employees', {})
        projects_raw = suivi_data.get('projects', {})
        tasks_raw = suivi_data.get('tasks', {})
        subtask_raw = suivi_data.get('subtasks', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        tasks = extract_data_list(tasks_raw)
        subtasks = extract_data_list(subtask_raw)
        
        
        # Vérification des erreurs de format
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):
            return "Erreur: Données corrompues", "Erreur: Données corrompues", "Erreur: Données corrompues"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):
            return "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible"
        
        try:
            # Fusion des données
            employee_suivi = create_merged_suivi_dataframe(employees, projects, tasks, subtasks)
            print(employee_suivi.columns)
            
            if employee_suivi is None or employee_suivi.empty:
                error_msg = "Erreur: Impossible de fusionner les données"
                return error_msg, error_msg, error_msg
            
            # Préparation des composants
            option_department = employee_suivi['department_id_y'].dropna().unique()
            option_employee_name = employee_suivi['employee_name'].unique()
            date_min = employee_suivi['start_date_x'].min()
            date_max = employee_suivi['start_date_x'].max()
            
            return (
                create_dropdown(label="Employee", options=option_employee_name, dropdown_id='dropdown_employee2'),
                generate_chip_selector(id="department2", label="Department", options=option_department, multiple=True),
                get_date_range_component(date_min, date_max, id="date-input2")
            )
        
        except Exception as e:
            error_msg = f"Erreur de traitement: {str(e)}"
            return error_msg, error_msg, error_msg
        

    @app.callback(
    Output("column-groups-basic", "rowData"),
    [
    Input('suivi-data', 'data'),
    Input('dropdown_employee2', "value"),
    Input('department2', 'value'),
    Input('date-input2', 'value'),
    ],
    prevent_initial_call=False
    )
    def table_value(suivi_data,dropdown_employee2=None, department2=None, date_range2=None):
        # print(suivi_data)
        # Cas d'erreur dès le départ
        if not suivi_data or (isinstance(suivi_data, dict) and 'error' in suivi_data and len(suivi_data) == 1):
            error_msg = f"Erreur: {suivi_data.get('error', 'Données manquantes')}"
            return error_msg, error_msg, error_msg
        
        # Extraction des données
        employees_raw = suivi_data.get('employees', {})
        projects_raw = suivi_data.get('projects', {})
        tasks_raw = suivi_data.get('tasks', {})
        subtasks_raw = suivi_data.get('subtasks', {})
        
        employees = extract_data_list(employees_raw)
        projects = extract_data_list(projects_raw)
        tasks = extract_data_list(tasks_raw)
        subtasks = extract_data_list(subtasks_raw)

        print(employees)
        
        
        # Vérification des erreurs de format
        if (isinstance(employees, dict) and 'error' in employees) or (isinstance(projects, dict) and 'error' in projects):
            return "Erreur: Données corrompues", "Erreur: Données corrompues", "Erreur: Données corrompues"
        
        if not employees or not projects or not isinstance(employees, list) or not isinstance(projects, list):
            return "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible", "Erreur: Aucune donnée disponible"
        
        try:
            # Fusion des données
            employee_suivi = create_merged_suivi_dataframe(employees, projects, tasks, subtasks)
            print(employee_suivi)
            
            if employee_suivi is None or employee_suivi.empty:
                error_msg = "Erreur: Impossible de fusionner les données"
                return error_msg, error_msg, error_msg
            
            @cache.memoize()
            def get_filtered_suivi_dataframe(dropdown_employee2, department2_tuple, start_date, end_date):
                """Récupère et filtre les données avec mise en cache"""
                department2 = list(department2_tuple) if department2_tuple else None
                return filter_data_performance(employee_suivi, dropdown_employee2,department2, start_date, end_date)

            start_date = None
            end_date = None
            if date_range2 and isinstance(date_range2, list) and len(date_range2) == 2:
                start_date = date_range2[0]
                end_date = date_range2[1]
                print(f"Date filtre: {start_date} à {end_date}")
            else:
                print(f"Date range invalide: {date_range2}")
        
            department2 = list(department2) if department2 else None
            filtered_suivi = get_filtered_suivi_dataframe(dropdown_employee2, department2,start_date,end_date)
            filtered_suivi['délai'] = (filtered_suivi['expected_end_date'] - filtered_suivi['end_date_x']).dt.days
            filtered_suivi['délai'] = filtered_suivi['délai'].fillna(0).astype(int)
            def maj_statut(row):
                if pd.notna(row['expected_end_date']) and pd.notna(row['end_date_x']):
                        if row['délai'] < 0:
                            return f"En retard({abs(row['délai'])}jr)"
                        else:
                            return row['status_x']  # conserve le statut existant sinon
                else:
                    return row['status_x']  # si dates manquantes, on ne change rien
                
            filtered_suivi['status_x'] = filtered_suivi.apply(maj_statut, axis=1)
    
            result=filtered_suivi[['employee_name','manager_task','project_name','tache_name','description_x','priority','progress_x',
                               'status_x','subtask_ids']]
            result.columns = ['Employee', 'Manager', 'projet','Tache', 'Description', 'Priorite', 'Progression', 'Statut',
                          'sous taches']
            result = result.reset_index(drop=True)
            result['sous taches'] = result['sous taches'].apply(lambda x: len(x) if isinstance(x, (list, str)) else 0)
        
            return result.to_dict('records')
       
        except Exception as e:
            error_msg = f"Erreur de traitement: {str(e)}"
            return error_msg,error_msg,error_msg,error_msg

    @app.callback(Output('page', 'children',),        
          Input('url1', 'pathname'),
          prevent_initial_call=False
           )
    def display_page(pathname):          
        if pathname == '/performances':
            return Performances.layout
        elif pathname == '/suivi':
            return Suivi.layout
        # elif pathname == '/':
        #     return loginpage.layout
        else:
            return analyse.layout
        
    @app.callback(
    [Output('nav-link-home', 'className'),
     Output('nav-link-performances', 'className'),
     Output('nav-link-suivi', 'className')],
    Input('url1', 'pathname'),
    prevent_initial_call=False
)
    def update_nav_links(pathname):
        base_class = "nav-link"
        active_class = "nav-link active"
        if pathname == '/performances':
            return base_class, active_class, base_class
        elif pathname == '/suivi':
            return base_class, base_class, active_class
        # elif pathname == '/':
        #     return base_class, base_class, active_class
        else:  # '/' ou défaut
            return active_class, base_class, base_class
    
    return app
    


# Point d'entrée principal
if __name__ == '__main__':
    print("Démarrage de l'application Dash...")
    app = create_dash_app()
    print("Lancement du serveur sur http://127.0.0.1:8050/dash/")
    app.run(host='127.0.0.1', port=8050)  # Correction: run_server au lieu de run


# first version
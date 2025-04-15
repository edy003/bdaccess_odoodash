# -*- coding: utf-8 -*-
import sys
print("Python utilisé :", sys.executable)

import dash
from dash import html,dcc, Input, Output
import logging
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import requests
import plotly.express as px




_logger = logging.getLogger(__name__)

def create_dash_app():
    
    """Créer et configurer l'application Dash"""
    app = dash.Dash(
        __name__,
        requests_pathname_prefix='/dash/',  # Corrige les erreurs de chemin derrière Nginx
        routes_pathname_prefix='/dash/',    # Corrige le loading infini
        assets_url_path='/dash/assets',
        external_stylesheets=[dbc.themes.BOOTSTRAP]     # Corrige le chargement des fichiers statiques
    )

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
    print(subtasks_df.head())


    tasks = get_tasks()

    if not tasks:
        _logger.warning("Aucune tâche récupérée")
        tasks = []

    tasks_df = pd.DataFrame(tasks)
    print(tasks_df.head())

    employee_ratings = get_employee_ratings()

    if not employee_ratings:
        _logger.warning("Aucune évaluation récupérée")
        employee_ratings = []
    ratings_df = pd.DataFrame(employee_ratings)
    print(ratings_df.head())
    
    project_deliveries = get_project_deliveries()

    if not project_deliveries:
       _logger.warning("Aucune livraison de projet récupérée")
       project_deliveries = []
    deliveries_df = pd.DataFrame(project_deliveries)
    print(deliveries_df.head())

    employee_data = get_employee_data()

    if not employee_data:
        _logger.warning("Aucune donnée d'employé n'a été récupérée")
        employee_data = []
    df = pd.DataFrame(employee_data)
    print(df.head())

    project_data = get_projects()

    if not project_data:
       _logger.warning("Aucun projet récupéré")
       project_data = []
    projects_df = pd.DataFrame(project_data)
    print(projects_df.head())


    
    
    
    
    

    
    

   
   
    
    # counts=df['role'].value_counts().reset_index()
    # counts.columns = ['role', 'count']
      # Affiche les 5 premières lignes du DataFrame pour le débogage
   
    
    # fig = px.pie(counts, values='count', names='role', title='Répartition des employés par rôle et statut de manager')
    

    # Layout simple
    app.layout = html.Div('hello',className='bg-secondary')
    

    return app

# Démarrage de l'application
if __name__ == '__main__':
    app = create_dash_app()
    app.run(debug=True, host='127.0.0.1', port=8050, dev_tools_ui=True)
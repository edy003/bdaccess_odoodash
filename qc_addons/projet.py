import pandas as pd
import json
import logging
from odoo import http
from odoo.http import request
from datetime import datetime

_logger = logging.getLogger(__name__)

class ProjectDashboardController(http.Controller):

    @http.route('/dashboard/project_count', type='json', auth='user', csrf=False)
    def get_project_count(self, project_type=None, partner_id=None, project_manager_id=None, department_ids=None):
        """
        Récupère le nombre total de projets avec filtres :
        - project_type : 'internal' ou 'external'
        - partner_id : ID du partenaire
        - project_manager_id : ID du chef de projet (user_id)
        - department_ids : Liste d'IDs de départements (Many2many)
        """
        try:
            _logger.info(
                f"Début de get_project_count avec filtres: "
                f"project_type={project_type}, partner_id={partner_id}, "
                f"project_manager={project_manager_id}, departments={department_ids}"
            )

            # Récupération de tous les projets
            projects = request.env['project.project'].sudo().search([])
            _logger.info(f"Trouvé {len(projects)} projets au total")

            if not projects:
                return {'total_projects': 0, 'error': False}

            # Préparation des données
            project_data_list = []
            for project in projects:
                project_data_list.append({
                    'id': project.id,
                    'name': project.name,
                    'project_type': project.project_type,
                    'partner_id': project.partner_id.id if project.partner_id else None,
                    'user_id': project.user_id.id if project.user_id else None,  # Chef de projet
                    'department_ids': [dept.id for dept in project.test_department_ids] if project.test_department_ids else [],
                })

            df = pd.DataFrame(project_data_list)
            if df.empty:
                return {'total_projects': 0, 'error': False}

            # Application des filtres
            filtered_df = self._apply_project_filters(df, project_type, partner_id, project_manager_id, department_ids)

            if filtered_df.empty:
                _logger.info("Aucun projet après filtres")
                return {'total_projects': 0, 'error': False}

            # Calcul du nombre total de projets
            total_projects = len(filtered_df)
            _logger.info(f"Nombre de projets après filtres: {total_projects}")

            return {
                'total_projects': total_projects,
                'error': False
            }

        except Exception as e:
            _logger.error(f"Erreur dans get_project_count: {str(e)}", exc_info=True)
            return {
                'error': True,
                'message': str(e),
                'total_projects': 0
            }

    @http.route('/dashboard/projects_due', type='json', auth='user', csrf=False)
    def get_projects_due(self, project_type=None, partner_id=None, project_manager_id=None, department_ids=None):
        """
        Retourne le nombre de projets DANS LES DÉLAIS (date de fin >= aujourd'hui)
        = Projets qui ne sont PAS encore en retard
        """
        try:
            today = datetime.now().date()
            _logger.info(f"📅 Date du jour: {today}")
            _logger.info(f"🔍 Filtres reçus: project_type={project_type}, partner_id={partner_id}, "
                         f"project_manager_id={project_manager_id}, department_ids={department_ids}")

            # 1️⃣ Récupération de tous les projets
            projects = request.env['project.project'].sudo().search([])
            _logger.info(f"📊 Total projets trouvés: {len(projects)}")

            if not projects:
                return {'total_projects': 0, 'error': False}

            # 2️⃣ Préparation des données
            project_data_list = []
            for project in projects:
                project_data_list.append({
                    'id': project.id,
                    'name': project.name,
                    'project_type': project.project_type,
                    'partner_id': project.partner_id.id if project.partner_id else None,
                    'user_id': project.user_id.id if project.user_id else None,
                    'department_ids': [dept.id for dept in project.test_department_ids] if project.test_department_ids else [],
                    'date': project.date,
                })

            df = pd.DataFrame(project_data_list)
            if df.empty:
                _logger.warning("⚠️ DataFrame vide après création")
                return {'total_projects': 0, 'error': False}

            _logger.info(f"📊 DataFrame créé avec {len(df)} projets")

            # 3️⃣ Filtrer les projets avec date définie
            df_with_dates = df[df['date'].notna()]
            _logger.info(f"📊 Projets avec date de fin définie: {len(df_with_dates)}/{len(df)}")
            if df_with_dates.empty:
                _logger.warning("⚠️ Aucun projet n'a de date de fin définie")
                return {'total_projects': 0, 'error': False}

            # 4️⃣ Convertir en format date
            df_with_dates = df_with_dates.copy()
            df_with_dates['date'] = pd.to_datetime(df_with_dates['date'], errors='coerce').dt.date

            # 5️⃣ Projets dans les délais (date >= aujourd'hui)
            df_in_time = df_with_dates[df_with_dates['date'] >= today]
            _logger.info(f"📊 Projets dans les délais (date >= {today}): {len(df_in_time)}")

            if df_in_time.empty:
                _logger.warning(f"⚠️ Aucun projet dans les délais!")
                return {'total_projects': 0, 'error': False}

            # 6️⃣ Application des filtres supplémentaires
            filtered_df = self._apply_project_filters(
                df_in_time,
                project_type,
                partner_id,
                project_manager_id,
                department_ids
            )

            total_projects = len(filtered_df)
            _logger.info(f"✅ Nombre final de projets dans les délais après tous les filtres: {total_projects}")

            return {'total_projects': total_projects, 'error': False}

        except Exception as e:
            _logger.error(f"❌ Erreur dans get_projects_due: {str(e)}", exc_info=True)
            return {'total_projects': 0, 'error': True, 'message': str(e)}
        

    @http.route('/dashboard/projects_late', type='json', auth='user', csrf=False)
    def get_projects_late(self, project_type=None, partner_id=None, project_manager_id=None, department_ids=None):
        """
        Retourne le nombre de projets EN RETARD (date de fin < aujourd'hui)
        """
        try:
            today = datetime.now().date()
            _logger.info(f"📅 Date du jour: {today}")
            _logger.info(f"🔍 Filtres reçus: project_type={project_type}, partner_id={partner_id}, "
                         f"project_manager_id={project_manager_id}, department_ids={department_ids}")

            # 1️⃣ Récupération de tous les projets
            projects = request.env['project.project'].sudo().search([])
            _logger.info(f"📊 Total projets trouvés: {len(projects)}")

            if not projects:
                return {'total_projects': 0, 'error': False}

            # 2️⃣ Préparation des données
            project_data_list = []
            for project in projects:
                project_data_list.append({
                    'id': project.id,
                    'name': project.name,
                    'project_type': project.project_type,
                    'partner_id': project.partner_id.id if project.partner_id else None,
                    'user_id': project.user_id.id if project.user_id else None,
                    'department_ids': [dept.id for dept in project.test_department_ids] if project.test_department_ids else [],
                    'date': project.date,
                })

            df = pd.DataFrame(project_data_list)
            if df.empty:
                _logger.warning("⚠️ DataFrame vide après création")
                return {'total_projects': 0, 'error': False}

            _logger.info(f"📊 DataFrame créé avec {len(df)} projets")

            # 3️⃣ Filtrer les projets avec date définie
            df_with_dates = df[df['date'].notna()]
            _logger.info(f"📊 Projets avec date de fin définie: {len(df_with_dates)}/{len(df)}")
            if df_with_dates.empty:
                _logger.warning("⚠️ Aucun projet n'a de date de fin définie")
                return {'total_projects': 0, 'error': False}

            # 4️⃣ Convertir en format date
            df_with_dates = df_with_dates.copy()
            df_with_dates['date'] = pd.to_datetime(df_with_dates['date'], errors='coerce').dt.date

            # 5️⃣ Filtrage des projets EN RETARD (date < aujourd'hui)
            df_late = df_with_dates[df_with_dates['date'] < today]
            _logger.info(f"📊 Projets en retard (date < {today}): {len(df_late)}")

            if df_late.empty:
                _logger.warning("⚠️ Aucun projet en retard")
                return {'total_projects': 0, 'error': False}

            # 6️⃣ Application des filtres supplémentaires
            filtered_df = self._apply_project_filters(
                df_late,
                project_type,
                partner_id,
                project_manager_id,
                department_ids
            )

            total_projects = len(filtered_df)
            _logger.info(f"✅ Nombre final de projets en retard après tous les filtres: {total_projects}")

            return {'total_projects': total_projects, 'error': False}

        except Exception as e:
            _logger.error(f"❌ Erreur dans get_projects_late: {str(e)}", exc_info=True)
            return {'total_projects': 0, 'error': True, 'message': str(e)}
        
    @http.route('/dashboard/departments_count', type='json', auth='user', csrf=False)
    def get_departments_count(self, project_type=None, partner_id=None, project_manager_id=None, department_ids=None):
        """
        Retourne le nombre de départements UNIQUES impliqués dans les projets (avec filtres)
        """
        try:
            _logger.info(f"🔍 Filtres reçus: project_type={project_type}, partner_id={partner_id}, "
                         f"project_manager_id={project_manager_id}, department_ids={department_ids}")

            # 1️⃣ Récupération de tous les projets
            projects = request.env['project.project'].sudo().search([])
            _logger.info(f"📊 Total projets trouvés: {len(projects)}")

            if not projects:
                return {'total_departments': 0, 'error': False}

            # 2️⃣ Préparation des données
            project_data_list = []
            for project in projects:
                project_data_list.append({
                    'id': project.id,
                    'name': project.name,
                    'project_type': project.project_type,
                    'partner_id': project.partner_id.id if project.partner_id else None,
                    'user_id': project.user_id.id if project.user_id else None,
                    'department_ids': [dept.id for dept in project.test_department_ids] if project.test_department_ids else [],
                })

            df = pd.DataFrame(project_data_list)
            if df.empty:
                _logger.warning("⚠️ DataFrame vide après création")
                return {'total_departments': 0, 'error': False}

            _logger.info(f"📊 DataFrame créé avec {len(df)} projets")

            # 3️⃣ Application des filtres
            filtered_df = self._apply_project_filters(
                df,
                project_type,
                partner_id,
                project_manager_id,
                department_ids
            )

            _logger.info(f"📊 Projets après filtres: {len(filtered_df)}")

            if filtered_df.empty:
                _logger.warning("⚠️ Aucun projet après application des filtres")
                return {'total_departments': 0, 'error': False}

            # 4️⃣ Extraction de tous les départements uniques
            all_departments = set()
            for dept_list in filtered_df['department_ids']:
                if isinstance(dept_list, list) and dept_list:
                    all_departments.update(dept_list)

            total_departments = len(all_departments)
            _logger.info(f"✅ Nombre de départements uniques impliqués: {total_departments}")
            _logger.info(f"📋 IDs des départements: {sorted(all_departments)}")

            return {
                'total_departments': total_departments,
                'department_ids': sorted(all_departments),  # Optionnel: liste des IDs
                'error': False
            }

        except Exception as e:
            _logger.error(f"❌ Erreur dans get_departments_count: {str(e)}", exc_info=True)
            return {'total_departments': 0, 'error': True, 'message': str(e)}
        


    @http.route('/dashboard/project_type_distribution', type='json', auth='user', csrf=False)
    def get_project_type_distribution(self, project_type=None, partner_id=None, project_manager_id=None, department_ids=None):
        """
        Retourne la répartition des projets par type (pour pie chart) avec filtres
        Format attendu par le frontend : { "chart_data": { "labels": [...], "values": [...] }, "error": false }
        """
        try:
            _logger.info(f"Filtres reçus: project_type={project_type}, partner_id={partner_id}, "
                         f"project_manager_id={project_manager_id}, department_ids={department_ids}")
            # 1. Récupération de tous les projets
            projects = request.env['project.project'].sudo().search([])
            _logger.info(f"Total projets trouvés: {len(projects)}")
            if not projects:
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
            # 2. Préparation des données
            project_data_list = []
            for project in projects:
                project_data_list.append({
                    'id': project.id,
                    'name': project.name,
                    'project_type': project.project_type or 'Non défini',
                    'partner_id': project.partner_id.id if project.partner_id else None,
                    'user_id': project.user_id.id if project.user_id else None,
                    'department_ids': [dept.id for dept in project.test_department_ids] if project.test_department_ids else [],
                })
            df = pd.DataFrame(project_data_list)
            if df.empty:
                _logger.warning("DataFrame vide après création")
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
            # 3. Application des filtres
            filtered_df = self._apply_project_filters(
                df,
                project_type,
                partner_id,
                project_manager_id,
                department_ids
            )
            _logger.info(f"Projets après filtres: {len(filtered_df)}")
            if filtered_df.empty:
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
            # 4. Calcul du nombre de projets par type
            type_counts = filtered_df['project_type'].fillna('Non défini').value_counts()
           
            # Conversion explicite en dict avec labels et values séparés (format Plotly)
            labels = type_counts.index.tolist()  # ex: ['internal', 'external', 'Non défini']
            values = type_counts.values.tolist()  # ex: [15, 28, 3]
            _logger.info(f"Répartition finale: {dict(zip(labels, values))}")
            return {
                'chart_data': {
                    'labels': labels,
                    'values': values
                },
                'error': False
            }
        except Exception as e:
            _logger.error(f"Erreur dans get_project_type_distribution: {str(e)}", exc_info=True)
            return {
                'chart_data': {'labels': [], 'values': []},
                'error': True,
                'message': str(e)
            }

    @http.route('/dashboard/projects_by_department', type='json', auth='user', csrf=False)
    def get_projects_by_department(self, project_type=None, partner_id=None, project_manager_id=None, department_ids=None):
        """
        Retourne la répartition des PROJETS par département (Many2many sur project.project)
        Format attendu par le frontend : { "chart_data": { "labels": [...], "values": [...] }, "error": false }
        """
        try:
            _logger.info(f"Filtres reçus: project_type={project_type}, partner_id={partner_id}, "
                         f"project_manager_id={project_manager_id}, department_ids={department_ids}")
            # 1. Récupération de tous les projets
            projects = request.env['project.project'].sudo().search([])
            _logger.info(f"Total projets trouvés: {len(projects)}")
            if not projects:
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
            # 2. Préparation des données
            project_data_list = []
            for project in projects:
                project_data_list.append({
                    'id': project.id,
                    'name': project.name,
                    'project_type': project.project_type or 'Non défini',
                    'partner_id': project.partner_id.id if project.partner_id else None,
                    'user_id': project.user_id.id if project.user_id else None,
                    'department_ids': [dept.id for dept in project.test_department_ids] if project.test_department_ids else [],
                })
            df = pd.DataFrame(project_data_list)
            if df.empty:
                _logger.warning("DataFrame vide après création")
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
            # 3. Application des filtres (exactement comme dans ton exemple)
            filtered_df = self._apply_project_filters(
                df,
                project_type,
                partner_id,
                project_manager_id,
                department_ids
            )
            _logger.info(f"Projets après filtres: {len(filtered_df)}")
            if filtered_df.empty:
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
            # 4. Exploser le champ Many2many + compter les projets par département
            exploded_df = filtered_df.explode('department_ids')
            exploded_df['department_ids'] = pd.to_numeric(exploded_df['department_ids'], errors='coerce')
            exploded_df = exploded_df.dropna(subset=['department_ids'])
            if exploded_df.empty:
                return {
                    'chart_data': {'labels': ['Aucun département'], 'values': [0]},
                    'error': False
                }
            # Comptage par département
            dept_counts = exploded_df['department_ids'].value_counts()
            # Récupérer les noms complets des départements
            dept_ids = dept_counts.index.astype(int).tolist()
            departments = request.env['hr.department'].sudo().browse(dept_ids)
            dept_name_map = {d.id: d.complete_name or d.name or f"Dépt {d.id}" for d in departments}
            # Préparer les labels et valeurs
            labels = [dept_name_map.get(int(did), f"Dépt {int(did)}") for did in dept_counts.index]
            values = dept_counts.values.tolist()
            # Tri décroissant (le plus grand en haut)
            sorted_pairs = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
            labels, values = zip(*sorted_pairs) if sorted_pairs else ([], [])
            _logger.info(f"Répartition finale projets par département: {dict(zip(labels, values))}")
            return {
                'chart_data': {
                    'labels': list(labels),
                    'values': list(values)
                },
                'error': False
            }
        except Exception as e:
            _logger.error(f"Erreur dans get_projects_by_department: {str(e)}", exc_info=True)
            return {
                'chart_data': {'labels': [], 'values': []},
                'error': True,
                'message': str(e)
            }

    @http.route('/dashboard/projects_by_manager', type='json', auth='user', csrf=False)
    def get_projects_by_manager(self, project_type=None, partner_id=None, project_manager_id=None, department_ids=None):
        """
        Retourne la répartition des PROJETS par Project Manager
        Format attendu par le frontend : { "chart_data": { "labels": [...], "values": [...] }, "error": false }
        """
        try:
            _logger.info(f"Filtres reçus: project_type={project_type}, partner_id={partner_id}, "
                         f"project_manager_id={project_manager_id}, department_ids={department_ids}")
           
            # 1. Récupération de tous les projets
            projects = request.env['project.project'].sudo().search([])
            _logger.info(f"Total projets trouvés: {len(projects)}")
           
            if not projects:
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
           
            # 2. Préparation des données
            project_data_list = []
            for project in projects:
                project_data_list.append({
                    'id': project.id,
                    'name': project.name,
                    'project_type': project.project_type or 'Non défini',
                    'partner_id': project.partner_id.id if project.partner_id else None,
                    'user_id': project.user_id.id if project.user_id else None, # ← Project Manager
                    'user_name': project.user_id.name if project.user_id else 'Non assigné',
                    'department_ids': [dept.id for dept in project.test_department_ids] if project.test_department_ids else [],
                })
           
            df = pd.DataFrame(project_data_list)
           
            if df.empty:
                _logger.warning("DataFrame vide après création")
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
           
            # 3. Application des filtres
            filtered_df = self._apply_project_filters(
                df,
                project_type,
                partner_id,
                project_manager_id,
                department_ids
            )
           
            _logger.info(f"Projets après filtres: {len(filtered_df)}")
           
            if filtered_df.empty:
                return {
                    'chart_data': {'labels': [], 'values': []},
                    'error': False
                }
           
            # 4. Comptage par Project Manager
            manager_counts = filtered_df['user_name'].value_counts()
           
            # Préparer les labels et valeurs
            labels = manager_counts.index.tolist()
            values = manager_counts.values.tolist()
           
            # Tri croissant (du plus petit au plus grand)
            sorted_pairs = sorted(zip(labels, values), key=lambda x: x[1])
            labels, values = zip(*sorted_pairs) if sorted_pairs else ([], [])
           
            _logger.info(f"Répartition finale projets par manager: {dict(zip(labels, values))}")
           
            return {
                'chart_data': {
                    'labels': list(labels),
                    'values': list(values)
                },
                'error': False
            }
           
        except Exception as e:
            _logger.error(f"Erreur dans get_projects_by_manager: {str(e)}", exc_info=True)
            return {
                'chart_data': {'labels': [], 'values': []},
                'error': True,
                'message': str(e)
            }
            

    @http.route('/dashboard/projects_table', type='json', auth='user', csrf=False)
    def get_projects_table(self, project_type=None, partner_id=None, project_manager_id=None, department_ids=None):
        """
        Version ROBUSTE avec Pandas + gestion d'erreurs complète
        """
        try:
            _logger.info("=" * 80)
            _logger.info(f"get_projects_table START")
            _logger.info(f" project_type={project_type}")
            _logger.info(f" partner_id={partner_id}")
            _logger.info(f" project_manager_id={project_manager_id}")
            _logger.info(f" department_ids={department_ids}")
            _logger.info("=" * 80)
           
            # 1. Récupération des projets (avec LIMIT de sécurité)
            projects = request.env['project.project'].sudo().search([], limit=5000)
            _logger.info(f"{len(projects)} projets récupérés de la base")
           
            if not projects:
                _logger.warning("Aucun projet trouvé dans la base")
                return {'data': [], 'error': False}
           
            # 2. Préparation des données (avec protection contre None)
            project_data_list = []
            for idx, project in enumerate(projects):
                try:
                    project_data_list.append({
                        'id': project.id,
                        'name': project.name or 'Sans nom',
                        'project_type': project.project_type if project.project_type else 'Non défini',
                        'partner_id': project.partner_id.id if project.partner_id else None,
                        'partner_name': project.partner_id.name if project.partner_id else 'N/A',
                        'user_id': project.user_id.id if project.user_id else None,
                        'user_name': project.user_id.name if project.user_id else 'Non assigné',
                        'project_assistant_name': project.project_assistant_id.name if project.project_assistant_id else 'N/A',
                        'practice_name': project.practice_id.name if project.practice_id else 'N/A',
                        'subcategories': ', '.join([sub.name for sub in project.subcategory_ids]) if project.subcategory_ids else 'N/A',
                        'department_ids': [dept.id for dept in project.test_department_ids] if project.test_department_ids else [],
                    })
                except Exception as e:
                    _logger.error(f"Erreur projet {project.id}: {str(e)}")
                    continue
           
            _logger.info(f"{len(project_data_list)} projets préparés")
           
            if not project_data_list:
                _logger.warning("Aucune donnée après préparation")
                return {'data': [], 'error': False}
           
            # 3. Création DataFrame avec gestion d'erreur
            try:
                df = pd.DataFrame(project_data_list)
                _logger.info(f"DataFrame créé: {len(df)} lignes, {len(df.columns)} colonnes")
                _logger.info(f" Colonnes: {df.columns.tolist()}")
            except Exception as e:
                _logger.error(f"Erreur création DataFrame: {str(e)}", exc_info=True)
                return {'data': [], 'error': True, 'message': f"Erreur Pandas: {str(e)}"}
           
            # 4. Application des filtres (avec protection)
            try:
                filtered_df = self._apply_project_filters(
                    df, project_type, partner_id, project_manager_id, department_ids
                )
                _logger.info(f"Filtres appliqués: {len(filtered_df)} lignes restantes")
            except Exception as e:
                _logger.error(f"Erreur filtrage: {str(e)}", exc_info=True)
                # En cas d'erreur de filtrage, on retourne TOUT
                filtered_df = df
           
            # 5. Conversion finale (avec protection contre les NaN)
            try:
                # Remplacer les NaN par des valeurs par défaut
                filtered_df = filtered_df.fillna({
                    'name': 'Sans nom',
                    'project_type': 'Non défini',
                    'partner_name': 'N/A',
                    'user_name': 'Non assigné',
                    'project_assistant_name': 'N/A',
                    'practice_name': 'N/A',
                    'subcategories': 'N/A'
                })
               
                # Supprimer les colonnes inutiles pour DataTable
                columns_to_keep = [
                    'id', 'name', 'project_type', 'partner_name',
                    'user_name', 'project_assistant_name', 'practice_name', 'subcategories'
                ]
               
                table_data = filtered_df[columns_to_keep].to_dict('records')
               
                _logger.info(f"{len(table_data)} projets prêts pour DataTable")
                _logger.info("=" * 80)
               
                return {'data': table_data, 'error': False}
               
            except Exception as e:
                _logger.error(f"Erreur conversion finale: {str(e)}", exc_info=True)
                return {'data': [], 'error': True, 'message': f"Erreur conversion: {str(e)}"}
           
        except Exception as e:
            _logger.error(f"ERREUR CRITIQUE get_projects_table: {str(e)}", exc_info=True)
            return {'data': [], 'error': True, 'message': str(e)}



    @http.route('/dashboard/project_types', type='json', auth='user',csrf=False)
    def get_project_types(self):
        """Retourne les types de projets disponibles"""
        try:
            return {
                'project_types': [
                    {'id': 'internal', 'name': 'Internal Project'},
                    {'id': 'external', 'name': 'External Project'}
                ],
                'error': False
            }
        except Exception as e:
            _logger.error(f"Erreur dans get_project_types: {str(e)}")
            return {'error': True, 'message': str(e), 'project_types': []}

    @http.route('/dashboard/partners', type='json', auth='user', csrf=False)
    def get_partners(self):
        """Retourne la liste des partenaires/clients"""
        try:
            partners = request.env['res.partner'].sudo().search([
                ('is_company', '=', True)
            ])
            partners_list = [
                {'id': p.id, 'name': p.name}
                for p in partners
            ]
            return {'partners': partners_list, 'error': False}
        except Exception as e:
            _logger.error(f"Erreur dans get_partners: {str(e)}")
            return {'error': True, 'message': str(e), 'partners': []}

    @http.route('/dashboard/project_managers', type='json', auth='user',csrf=False)
    def get_project_managers(self):
        """Retourne la liste des chefs de projet (utilisateurs ayant des projets)"""
        try:
            projects = request.env['project.project'].sudo().search([
                ('user_id', '!=', False)
            ])
            managers = projects.mapped('user_id')
            managers_set = list(set(managers))
            managers_list = [
                {'id': m.id, 'name': m.name}
                for m in managers_set
            ]
            managers_list.sort(key=lambda x: x['name'])
            return {'managers': managers_list, 'error': False}
        except Exception as e:
            _logger.error(f"Erreur dans get_project_managers: {str(e)}")
            return {'error': True, 'message': str(e), 'managers': []}

    # ==================================================================
    # MÉTHODE PRIVÉE : Application des filtres
    # ==================================================================
    # def _apply_project_filters(self, df, project_type, partner_id, project_manager_id, department_ids):
    #     """Applique les filtres sur le DataFrame des projets"""
    #     filtered_df = df.copy()

    #     # Filtre par type de projet
    #     if project_type and project_type != "" and project_type != "null":
    #         _logger.info(f"Filtre project_type appliqué: {project_type}")
    #         filtered_df = filtered_df[filtered_df['project_type'] == project_type]

    #     # Filtre par partenaire
    #     if partner_id and partner_id != "" and partner_id != "null":
    #         try:
    #             partner_id_int = int(partner_id)
    #             _logger.info(f"Filtre partner_id appliqué: {partner_id_int}")
    #             filtered_df = filtered_df[filtered_df['partner_id'] == partner_id_int]
    #         except (ValueError, TypeError):
    #             _logger.warning(f"ID partenaire invalide: {partner_id}")

    #     # Filtre par chef de projet
    #     if project_manager_id and project_manager_id != "" and project_manager_id != "null":
    #         try:
    #             manager_id_int = int(project_manager_id)
    #             _logger.info(f"Filtre project_manager appliqué: {manager_id_int}")
    #             filtered_df = filtered_df[filtered_df['user_id'] == manager_id_int]
    #         except (ValueError, TypeError):
    #             _logger.warning(f"ID manager invalide: {project_manager_id}")

    #     # Filtre par départements (Many2many)
    #     if department_ids and department_ids != "" and department_ids != "null":
    #         try:
    #             # Si c'est une chaîne JSON
    #             if isinstance(department_ids, str):
    #                 dept_list = json.loads(department_ids)
    #             elif isinstance(department_ids, list):
    #                 dept_list = department_ids
    #             else:
    #                 dept_list = [int(department_ids)]

    #             _logger.info(f"Filtre departments appliqué: {dept_list}")

    #             # Filtrer les projets qui ont au moins un département dans la liste
    #             filtered_df = filtered_df[
    #                 filtered_df['department_ids'].apply(
    #                     lambda x: any(dept_id in x for dept_id in dept_list)
    #                     if isinstance(x, list) and x else False
    #                 )
    #             ]
    #         except (ValueError, TypeError, json.JSONDecodeError) as e:
    #             _logger.warning(f"Erreur lors du parsing des IDs départements: {e}")

    #     return filtered_df
    

    def _apply_project_filters(self, df, project_type, partner_id, project_manager_id, department_ids):
        """Applique les filtres sur le DataFrame des projets"""
        filtered_df = df.copy()
        # Filtre par type de projet
        if project_type and project_type not in ["", "null", None]: # AJOUT DE None
            _logger.info(f"Filtre project_type appliqué: {project_type}")
            filtered_df = filtered_df[filtered_df['project_type'] == project_type]
        # Filtre par partenaire
        if partner_id and partner_id not in ["", "null", None]: # AJOUT DE None
            try:
                partner_id_int = int(partner_id)
                _logger.info(f"Filtre partner_id appliqué: {partner_id_int}")
                filtered_df = filtered_df[filtered_df['partner_id'] == partner_id_int]
            except (ValueError, TypeError):
                _logger.warning(f"ID partenaire invalide: {partner_id}")
        # Filtre par chef de projet
        if project_manager_id and project_manager_id not in ["", "null", None]: # AJOUT DE None
            try:
                manager_id_int = int(project_manager_id)
                _logger.info(f"Filtre project_manager appliqué: {manager_id_int}")
                filtered_df = filtered_df[filtered_df['user_id'] == manager_id_int]
            except (ValueError, TypeError):
                _logger.warning(f"ID manager invalide: {project_manager_id}")
        # Filtre par départements (Many2many)
        if department_ids and department_ids not in ["", "null", None]: # AJOUT DE None
            try:
                # Si c'est une chaîne JSON
                if isinstance(department_ids, str):
                    dept_list = json.loads(department_ids)
                elif isinstance(department_ids, list):
                    dept_list = department_ids
                else:
                    dept_list = [int(department_ids)]
                _logger.info(f"Filtre departments appliqué: {dept_list}")
                # Filtrer les projets qui ont au moins un département dans la liste
                filtered_df = filtered_df[
                    filtered_df['department_ids'].apply(
                        lambda x: any(dept_id in x for dept_id in dept_list)
                        if isinstance(x, list) and x else False
                    )
                ]
            except (ValueError, TypeError, json.JSONDecodeError) as e:
                _logger.warning(f"Erreur lors du parsing des IDs départements: {e}")
        return filtered_df
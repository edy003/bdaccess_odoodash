# -*- coding: utf-8 -*-
# from odoo import http


# class Qctracker(http.Controller):
#     @http.route('/qctracker/qctracker', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qctracker/qctracker/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('qctracker.listing', {
#             'root': '/qctracker/qctracker',
#             'objects': http.request.env['qctracker.qctracker'].search([]),
#         })

#     @http.route('/qctracker/qctracker/objects/<model("qctracker.qctracker"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qctracker.object', {
#             'object': obj
#         })


# class EmployeeDataController(http.Controller):

#     @http.route('/api/get_employee_data1', type='http', auth='none', csrf=False, sitemap=False)
#     def get_employee_data(self, **kwargs):
#         """Endpoint JWT sécurisé via header, cookie ou paramètre URL"""

#         token = None

#         # 1. Essayer d'abord via le paramètre URL 'token'
#         if kwargs.get('token'):
#             token = kwargs.get('token')
#         else:
#             # 2. Sinon, essayer via le header Authorization
#             auth_header = request.httprequest.headers.get('Authorization')
#             if auth_header and auth_header.startswith('Bearer '):
#                 token = auth_header.split(' ')[1]
#             else:
#                 # 3. En dernier recours, essayer via le cookie HttpOnly
#                 token = request.httprequest.cookies.get('jwt_token')

#         if not token:
#             return request.make_response(
#                 json.dumps({'error': 'Token JWT manquant'}),
#                 headers=[('Content-Type', 'application/json')],
#                 status=401
#             )

#         try:
#             # Décodage du JWT
#             payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

#             # Récupérer l'ID utilisateur depuis le payload
#             user_id = payload.get('user_id')

#             # Accès aux employés
#             employees = request.env['qctracker.employee'].sudo().search([])
#             employee_list = []
#             for employee in employees:
#                 employee_data = {
#                     'employee_id': employee.id,
#                     'employee_name': employee.name,
#                     'role': employee.role,
#                     'country_id': employee.country_id.name if employee.country_id else "Sans pays",
#                     'is_manager': employee.is_manager,
#                     'gender': employee.gender,
#                     'department_id': employee.department_id.name if employee.department_id else "Sans département",
#                     'task_ids': employee.task_ids.ids,
#                     'rating_employee_ids': employee.rating_employee_ids.ids,
#                     'skill_rating_ids': employee.skill_rating_ids.ids,
#                     'project_ids': employee.project_ids.ids,
#                     'project_delivery_ids': employee.project_delivery_ids.ids,
#                 }
#                 employee_list.append(employee_data)

#             return request.make_response(
#                 json.dumps(employee_list),
#                 headers=[('Content-Type', 'application/json')]
#             )

#         except jwt.ExpiredSignatureError:
#             return request.make_response(
#                 json.dumps({'error': 'Token expiré'}),
#                 headers=[('Content-Type', 'application/json')],
#                 status=401
#             )

#         except jwt.InvalidTokenError:
#             return request.make_response(
#                 json.dumps({'error': 'Token invalide'}),
#                 headers=[('Content-Type', 'application/json')],
#                 status=401
#             )

# class DashboardController(http.Controller):

#     @http.route('/dashboard/token', auth='user', type='json')
#     def dashboard_token(self):
#         user = request.env.user
#         payload = {
#             "user_id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "exp": datetime.datetime.now() + datetime.timedelta(hours=1),
#         }
#         token = jwt.encode(payload, 'qc_secret', algorithm='HS256')
#         return {'token': token}


# # === Contrôleur : Données des employés ===
# class QCTrackerEmployeeController(http.Controller):

#     @http.route('/api/get_employee_data', type='http',  
#                 cors='*', auth='public'
#                 #  auth='custom_auth',sitemap=False
#                  )
#     def get_employee_data(self, **kwargs):
#         try:
            
#             employees = request.env['qctracker.employee'].sudo().search([])
#             employee_list = []

#             for employee in employees:
#                 employee_data = {
#                     'employee_id': employee.id,
#                     'employee_name': employee.name,
#                     'role': employee.role,
#                     'country_id': employee.country_id.name if employee.country_id else "Sans pays",
#                     'is_manager': employee.is_manager,
#                     'gender': employee.gender,
#                     'department_id': employee.department_id.name if employee.department_id else "Sans département",
#                     'task_ids': employee.task_ids.ids if employee.task_ids else [],
#                     'rating_employee_ids': employee.rating_employee_ids.ids if employee.rating_employee_ids else [],
#                     'skill_rating_ids': employee.skill_rating_ids.ids if employee.skill_rating_ids else [],
#                     'project_ids': employee.project_ids.ids if employee.project_ids else [],
#                     'project_delivery_ids': employee.project_delivery_ids.ids if employee.project_delivery_ids else [],
#                 }

#                 employee_list.append(employee_data)

#             return request.make_response(
#                 json.dumps(employee_list),
#                 headers=[('Content-Type', 'application/json')]
#             )

#         except Exception as e:
#             _logger.error(f"Erreur lors de la récupération des données employés : {e}")
#             return request.make_response(
#                 json.dumps([]),
#                 headers=[('Content-Type', 'application/json')]
#             )


#   @http.route('/get_tasks', type='http', auth='public', cors='*')
#     def get_tasks(self, **kwargs):
#         try:
#             tasks = request.env['qctracker.task'].sudo().search([])
#             task_list = []

#             for task in tasks:
#                 task_data = {
#                     'tache_id':task.id,
#                     'tache_name': task.name,
#                     'description': task.description or "",
#                     'employee': task.employee_id.id if task.employee_id else "Inconnu",
#                     'manager': task.manager_id.name if task.manager_id else "Inconnu",
#                     'project': task.project_id.id if task.project_id else "Aucun projet",
#                     'start_date': task.start_date.isoformat() if task.start_date else "",
#                     'expected_end_date': task.expected_end_date.isoformat() if task.expected_end_date else "",
#                     'end_date': task.end_date.isoformat() if task.end_date else "",
#                     'progress': task.progress,
#                     'priority': dict(task._fields['priority'].selection).get(task.priority, "Non défini"),
#                     'status': dict(task._fields['status'].selection).get(task.status, "Non défini"),
#                     'subtask_ids': [sub.id for sub in task.subtask_ids],
#                 }
#                 task_list.append(task_data)

#             return request.make_response(
#                 json.dumps(task_list),
#                 headers=[('Content-Type', 'application/json')]
#             )
#         except Exception as e:
#             _logger.error(f"Erreur lors de la récupération des tâches : {e}")
#             return request.make_response(
#                 json.dumps([]),
#                 headers=[('Content-Type', 'application/json')]
#             )

from odoo import http
from odoo.http import request
import json
import logging
from datetime import date, datetime
from odoo.http import Response
from odoo import api, SUPERUSER_ID
from werkzeug.wrappers import Response
import jwt
import odoo
import datetime
from jwt import ExpiredSignatureError, InvalidTokenError




_logger = logging.getLogger(__name__)


SECRET_KEY = "votre_cle_secrete_tres_longue_et_aleatoire"  # Utilisez une clé sécurisée en production!

class AuthController(http.Controller):
    
    @http.route('/api/auth/login', type='json', auth='none', csrf=False, methods=['POST'])
    def login(self, **kw):
        """Endpoint d'authentification qui génère un JWT"""
        
        # Récupérer les données de la requête
        data = json.loads(request.httprequest.data.decode('utf-8'))
        login = data.get('login')
        password = data.get('password')
        
        if not login or not password:
            return {'success': False, 'error': 'Login et mot de passe requis'}
        
        # Authentifier l'utilisateur avec Odoo
        uid = request.session.authenticate(request.session.db, login, password)
        
        if not uid:
            return {'success': False, 'error': 'Identifiants invalides'}
        
        # Récupérer l'utilisateur
        user = request.env['res.users'].sudo().browse(uid)
        role = 'employee'  # Par défaut
        if user.has_group('base.group_system'):
            role = 'admin'
        elif user.has_group('base.group_user'):
            role = 'employee'
        
        # Créer les données du payload JWT
        payload = {
            'user_id': uid,
            'login': user.login,
            'name': user.name,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1) , # Expiration dans 1 jour
            'role':role
        }
        
        # Générer le token JWT
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        # Si jwt.encode retourne des bytes (dépend de la version de PyJWT)
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        return {
            'success': True,
            'user': {
                'id': uid,
                'name': user.name,
                'login': user.login,
                'role': role
            },
            'token': token
        }

       
class DashController(http.Controller):

    @http.route('/dash/', type='http', auth='user', website=True)
    def serve_dash(self, **kwargs):
        """Affiche une page avec une iframe pour intégrer Dash dans Odoo"""
        return request.render('qctracker.qctracker_dashboard_view', {
            'dash': "http://127.0.0.1:8050/dash"
        })



class QCTrackerEmployeeController(http.Controller):

    @http.route('/api/get_employee_data', type='http', auth='none', csrf=False, methods=['GET'])
    def get_employee_data(self, **kwargs):
        try:
            auth_header = request.httprequest.headers.get('Authorization')
            if not auth_header:
                response_data = {'success': False, 'error': 'Token manquant'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
            
            token = auth_header.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            uid = payload.get('user_id')
            user = request.env['res.users'].sudo().browse(uid)
            
            if not user.exists():
                response_data = {'success': False, 'error': 'Utilisateur non trouvé'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
            
            role = payload.get('role')
            employee_obj = request.env['qctracker.employee'].sudo()
            
            if role == 'admin' or user.has_group('base.group_system'):
                employees = employee_obj.search([])
            else:
                employees = employee_obj.search([('user_id', '=', user.id)])
            
            employee_list = []
            for employee in employees:
                employee_data = {
                    'employee_id': employee.id,
                    'employee_name': employee.name,
                    'role': employee.role,
                    'country_id': employee.country_id.name if employee.country_id else "Sans pays",
                    'is_manager': employee.is_manager,
                    'gender': employee.gender,
                    'department_id': employee.department_id.name if employee.department_id else "Sans département",
                    'task_ids': employee.task_ids.ids if employee.task_ids else [],
                    'rating_employee_ids': employee.rating_employee_ids.ids if employee.rating_employee_ids else [],
                    'skill_rating_ids': employee.skill_rating_ids.ids if employee.skill_rating_ids else [],
                    'project_ids': employee.project_ids.ids if employee.project_ids else [],
                    'project_delivery_ids': employee.project_delivery_ids.ids if employee.project_delivery_ids else [],
                }
                employee_list.append(employee_data)
            
            response_data = {
                'success': True,
                'employees': employee_list,
                'user_role': role
            }
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
            
        except ExpiredSignatureError:
            response_data = {'success': False, 'error': 'Token expiré'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except InvalidTokenError:
            response_data = {'success': False, 'error': 'Token invalide'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des données employés : {e}", exc_info=True)
            response_data = {'success': False, 'error': str(e)}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])


# # # === Contrôleur : Évaluations des employés ===
class QCTrackerRatingController(http.Controller):

    @http.route('/api/get_employee_ratings', type='http', auth='none', csrf=False, methods=['GET'])
    def get_employee_ratings(self, **kwargs):
        try:
            auth_header = request.httprequest.headers.get('Authorization')
            if not auth_header:
                response_data = {'success': False, 'error': 'Token manquant'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            token = auth_header.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            uid = payload.get('user_id')
            user = request.env['res.users'].sudo().browse(uid)

            if not user.exists():
                response_data = {'success': False, 'error': 'Utilisateur non trouvé'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            role = payload.get('role')
            rating_obj = request.env['qctracker.employeerating'].sudo()

            # Si admin ou superuser, il peut voir toutes les notations
            if role == 'admin' or user.has_group('base.group_system'):
                ratings = rating_obj.search([])
            else:
                # Sinon, on limite aux notations faites par ce manager
                ratings = rating_obj.search([('manager_id', '=', user.employee_id.id)])

            rating_list = []

            for rating in ratings:
                rating_data = {
                    'employee_rate': rating.employee_id.id if rating.employee_id else "Inconnu",
                    'tache_name': rating.task_id.name if rating.task_id else "Aucune tâche",
                    'rating': rating.rating,
                    'on_time': rating.on_time,
                    'comments': rating.comments,
                    'evaluation_date': rating.evaluation_date.isoformat() if rating.evaluation_date else None,
                    'state': rating.state,
                    'manager': rating.manager_id.name if rating.manager_id else "Inconnu",       
                }
                rating_list.append(rating_data)

            response_data = {
                'success': True,
                'ratings': rating_list,
                'user_role': role
            }

            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')]
            )

        except ExpiredSignatureError:
            response_data = {'success': False, 'error': 'Token expiré'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except InvalidTokenError:
            response_data = {'success': False, 'error': 'Token invalide'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des évaluations : {e}", exc_info=True)
            response_data = {'success': False, 'error': str(e)}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])


# === Contrôleur : Livraisons de projets ===
# class QCTrackerProjectDeliveryController(http.Controller):
class QCTrackerProjectDeliveryController(http.Controller):

    @http.route('/api/get_project_deliveries', type='http', auth='none', csrf=False, methods=['GET'])
    def get_project_deliveries(self, **kwargs):
        try:
            auth_header = request.httprequest.headers.get('Authorization')
            if not auth_header:
                response_data = {'success': False, 'error': 'Token manquant'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            token = auth_header.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            uid = payload.get('user_id')
            user = request.env['res.users'].sudo().browse(uid)

            if not user.exists():
                response_data = {'success': False, 'error': 'Utilisateur non trouvé'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            role = payload.get('role')
            delivery_obj = request.env['qctracker.projectdelivery'].sudo()

            # Si admin ou superuser, il peut voir toutes les livraisons
            if role == 'admin' or user.has_group('base.group_system'):
                deliveries = delivery_obj.search([])
            else:
                # Sinon, on limite aux livraisons assignées à ce manager
                deliveries = delivery_obj.search([('employee_id', '=', user.employee_id.id)])

            delivery_list = []

            for delivery in deliveries:
                delivery_data = {
                    'project_id': delivery.project_id.name if delivery.project_id else "Inconnu",
                    'manager_project': delivery.employee_id.name if delivery.employee_id else "Inconnu",
                    'on_time': delivery.on_time,
                    'comments': delivery.comments,
                    'delivery_date': delivery.delivery_date.isoformat(),
                }
                delivery_list.append(delivery_data)

            response_data = {
                'success': True,
                'deliveries': delivery_list,
                'user_role': role
            }

            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')]
            )

        except ExpiredSignatureError:
            response_data = {'success': False, 'error': 'Token expiré'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except InvalidTokenError:
            response_data = {'success': False, 'error': 'Token invalide'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des livraisons de projet : {e}", exc_info=True)
            response_data = {'success': False, 'error': str(e)}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
    
class QCTrackerProjectController(http.Controller):

    @http.route('/api/get_projects', type='http', auth='none', csrf=False, methods=['GET'])
    def get_projects(self, **kwargs):
        try:
            auth_header = request.httprequest.headers.get('Authorization')
            if not auth_header:
                response_data = {'success': False, 'error': 'Token manquant'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            token = auth_header.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            uid = payload.get('user_id')
            user = request.env['res.users'].sudo().browse(uid)

            if not user.exists():
                response_data = {'success': False, 'error': 'Utilisateur non trouvé'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            role = payload.get('role')
            project_obj = request.env['qctracker.project'].sudo()

            # Si admin ou superuser, accès à tous les projets
            if role == 'admin' or user.has_group('base.group_system'):
                projects = project_obj.search([])
            else:
                # Si manager, accès aux projets assignés au manager
                projects = project_obj.search([('employee_id', '=', user.employee_id.id)])

            project_list = []

            for project in projects:
                project_data = {
                    'project_id': project.id,
                    'project_name': project.name,
                    'description': project.description or "",
                    'department_id': project.department_id.name if project.department_id else "Inconnu",
                    'start_date': project.start_date.isoformat() if project.start_date else None,
                    'end_date': project.end_date.isoformat() if project.end_date else None,
                    'employee_project': project.employee_id.name if project.employee_id else "Inconnu",
                    'status': project.status,
                    'progress': project.progress,
                    # 'tags': [tag.name for tag in project.tag_ids],
                    'project_delivery_ids':project.project_delivery_ids.ids if project.project_delivery_ids else [],
                    'task_project': project.task_ids.ids if project.task_ids else [],
                }
                project_list.append(project_data)

            response_data = {
                'success': True,
                'projects': project_list,
                'user_role': role
            }

            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')]
            )

        except ExpiredSignatureError:
            response_data = {'success': False, 'error': 'Token expiré'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except InvalidTokenError:
            response_data = {'success': False, 'error': 'Token invalide'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des projets : {e}", exc_info=True)
            response_data = {'success': False, 'error': str(e)}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

class QCTrackertaskController(http.Controller):

    @http.route('/api/get_tasks', type='http', auth='none', csrf=False, methods=['GET'])
    def get_tasks(self, **kwargs):
        try:
            auth_header = request.httprequest.headers.get('Authorization')
            if not auth_header:
                response_data = {'success': False, 'error': 'Token manquant'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            token = auth_header.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            uid = payload.get('user_id')
            user = request.env['res.users'].sudo().browse(uid)

            if not user.exists():
                response_data = {'success': False, 'error': 'Utilisateur non trouvé'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            role = payload.get('role')
            task_obj = request.env['qctracker.task'].sudo()

            # Récupération des tâches
            if role == 'admin' or user.has_group('base.group_system'):
                tasks = task_obj.search([])
            else:
                # Récupération des tâches assignées à l'employé ou gérées par le manager
                tasks = task_obj.search(['|', ('employee_id.user_id', '=', user.id), ('manager_id.id', '=', user.employee_id.id)])

            task_list = []

            for task in tasks:
                task_data = {
                    'tache_id':task.id,
                    'tache_name': task.name,
                    'description': task.description or "",
                    'employee_task': task.employee_id.id if task.employee_id else "Inconnu",
                    'manager_task': task.manager_id.name if task.manager_id else "Inconnu",
                    'project_task': task.project_id.id if task.project_id else "Aucun projet",
                    'start_date': task.start_date.isoformat() if task.start_date else "",
                    'expected_end_date': task.expected_end_date.isoformat() if task.expected_end_date else "",
                    'end_date': task.end_date.isoformat() if task.end_date else "",
                    'progress': task.progress,
                    'priority': dict(task._fields['priority'].selection).get(task.priority, "Non défini"),
                    'status': dict(task._fields['status'].selection).get(task.status, "Non défini"),
                    'subtask_ids': [sub.id for sub in task.subtask_ids],
                }
                task_list.append(task_data)

            response_data = {
                'success': True,
                'tasks': task_list,
                'user_role': role
            }

            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')]
            )

        except ExpiredSignatureError:
            response_data = {'success': False, 'error': 'Token expiré'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except InvalidTokenError:
            response_data = {'success': False, 'error': 'Token invalide'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des tâches : {e}", exc_info=True)
            response_data = {'success': False, 'error': str(e)}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        
class QCTrackersubtaskController(http.Controller):

    @http.route('/api/get_subtasks', type='http', auth='none', csrf=False, methods=['GET'])
    def get_subtasks(self, **kwargs):
        try:
            auth_header = request.httprequest.headers.get('Authorization')
            if not auth_header:
                response_data = {'success': False, 'error': 'Token manquant'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            token = auth_header.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            uid = payload.get('user_id')
            user = request.env['res.users'].sudo().browse(uid)

            if not user.exists():
                response_data = {'success': False, 'error': 'Utilisateur non trouvé'}
                return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])

            role = payload.get('role')
            subtask_obj = request.env['qctracker.subtask'].sudo()

            # Récupération des sous-tâches
            if role == 'admin' or user.has_group('base.group_system'):
                subtasks = subtask_obj.search([])
            else:
                # Récupérer uniquement les sous-tâches de l'utilisateur ou gérées par lui via la tâche associée
                subtasks = subtask_obj.search([
                    '|',
                    ('employee_id.user_id', '=', user.id),
                    ('task_id.manager_id.id', '=', user.employee_id.id)
                ])

            subtask_list = []

            for sub in subtasks:
                subtask_data = {
                    'subtask_id':sub.id,
                    'subtask_name': sub.name,
                    'description': sub.description or "",
                    'task': sub.task_id.id if sub.task_id else "Aucune tâche",
                    'employee_subtask': sub.employee_id.name if sub.employee_id else "Inconnu",
                    'start_date': sub.start_date.isoformat() if sub.start_date else "",
                    'end_date': sub.end_date.isoformat() if sub.end_date else "",
                    'status': dict(sub._fields['status'].selection).get(sub.status, "Non défini")
                }
                subtask_list.append(subtask_data)

            response_data = {
                'success': True,
                'subtasks': subtask_list,
                'user_role': role
            }

            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')]
            )

        except ExpiredSignatureError:
            response_data = {'success': False, 'error': 'Token expiré'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except InvalidTokenError:
            response_data = {'success': False, 'error': 'Token invalide'}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des sous-tâches : {e}", exc_info=True)
            response_data = {'success': False, 'error': str(e)}
            return request.make_response(json.dumps(response_data), headers=[('Content-Type', 'application/json')])
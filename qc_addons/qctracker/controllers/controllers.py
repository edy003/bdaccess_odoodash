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
from odoo import http
from odoo.http import request
import json
import logging
_logger = logging.getLogger(__name__)

class DashController(http.Controller):

    @http.route('/dashboard/dash/', type='http', auth='user', website=True)
    def serve_dash(self, **kwargs):
        """Affiche une page avec une iframe pour intégrer Dash dans Odoo"""
        return request.render('qctracker.qctracker_dashboard_view', {
            'dash_url': "http://127.0.0.1:8050/dash/"
        })

# === Contrôleur : Données des employés ===
class QCTrackerEmployeeController(http.Controller):

    @http.route('/get_employee_data', type='http', auth='public', cors='*')
    def get_employee_data(self, **kwargs):
        try:
            employees = request.env['qctracker.employee'].sudo().search([])
            employee_list = []

            for employee in employees:
                employee_data = {
                    'id': employee.id,
                    'name': employee.name,
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

            return request.make_response(
                json.dumps(employee_list),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des données employés : {e}")
            return request.make_response(
                json.dumps([]),
                headers=[('Content-Type', 'application/json')]
            )


# === Contrôleur : Évaluations des employés ===
# class QCTrackerRatingController(http.Controller):

    @http.route('/get_employee_ratings', type='http', auth='public', cors='*')
    def get_employee_ratings(self, **kwargs):
        _logger.info("Appel de /get_employee_ratings")
        try:
            ratings = request.env['qctracker.employeerating'].sudo().search([])
            rating_list = []

            for rating in ratings:
                rating_data = {
                    'employee': rating.employee_id.id if rating.employee_id else "Inconnu",
                    'task': rating.task_id.name if rating.task_id else "Aucune tâche",
                    'rating': rating.rating,
                    'on_time': rating.on_time,
                    'comments': rating.comments,
                    'evaluation_date': rating.evaluation_date.isoformat(),
                    'state': rating.state,
                    'manager': rating.manager_id.name if rating.manager_id else "Inconnu",       
                }
                rating_list.append(rating_data)

            return request.make_response(
                json.dumps(rating_list),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des évaluations : {e}")
            return request.make_response(
                json.dumps([]),
                headers=[('Content-Type', 'application/json')]
            )


# === Contrôleur : Livraisons de projets ===
# class QCTrackerProjectDeliveryController(http.Controller):

    @http.route('/get_project_deliveries', type='http', auth='public', cors='*')
    def get_project_deliveries(self, **kwargs):
        try:
            deliveries = request.env['qctracker.projectdelivery'].sudo().search([])
            delivery_list = []

            for delivery in deliveries:
                delivery_data = {
                    'project': delivery.project_id.name if delivery.project_id else "Inconnu",
                    'manager': delivery.employee_id.name if delivery.employee_id else "Inconnu",
                    'on_time': delivery.on_time,
                    'comments': delivery.comments,
                    'delivery_date': delivery.delivery_date.isoformat(),
                }
                delivery_list.append(delivery_data)

            return request.make_response(
                json.dumps(delivery_list),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des livraisons de projet : {e}")
            return request.make_response(
                json.dumps([]),
                headers=[('Content-Type', 'application/json')]
            )
    

    @http.route('/get_projects', type='http', auth='public', cors='*')
    def get_projects(self, **kwargs):
        try:
            projects = request.env['qctracker.project'].sudo().search([])
            project_list = []

            for project in projects:
                project_data = {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description or "",
                    'department_id': project.department_id.name if project.department_id else "Inconnu",
                    'start_date': project.start_date.isoformat() if project.start_date else None,
                    'end_date': project.end_date.isoformat() if project.end_date else None,
                    'employee_id': project.employee_id.name if project.employee_id else "Inconnu",
                    'status': project.status,
                    'progress': project.progress,
                    # 'tags': [tag.name for tag in project.tag_ids],
                    'project_delivery_ids':project.project_delivery_ids.ids if project.project_delivery_ids else [],
                    'task_ids': project.task_ids.ids if project.task_ids else [],
                }
                project_list.append(project_data)

            return request.make_response(
                json.dumps(project_list),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            _logger.error(f" Erreur lors de la récupération des projets : {e}")
            return request.make_response(
                json.dumps([]),
                headers=[('Content-Type', 'application/json')]
            )
        
    @http.route('/get_tasks', type='http', auth='public', cors='*')
    def get_tasks(self, **kwargs):
        try:
            tasks = request.env['qctracker.task'].sudo().search([])
            task_list = []

            for task in tasks:
                task_data = {
                    'tache_id':task.id,
                    'name': task.name,
                    'description': task.description or "",
                    'employee': task.employee_id.id if task.employee_id else "Inconnu",
                    'manager': task.manager_id.name if task.manager_id else "Inconnu",
                    'project': task.project_id.id if task.project_id else "Aucun projet",
                    'start_date': task.start_date.isoformat() if task.start_date else "",
                    'expected_end_date': task.expected_end_date.isoformat() if task.expected_end_date else "",
                    'end_date': task.end_date.isoformat() if task.end_date else "",
                    'progress': task.progress,
                    'priority': dict(task._fields['priority'].selection).get(task.priority, "Non défini"),
                    'status': dict(task._fields['status'].selection).get(task.status, "Non défini"),
                    'subtask_ids': [sub.id for sub in task.subtask_ids],
                }
                task_list.append(task_data)

            return request.make_response(
                json.dumps(task_list),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des tâches : {e}")
            return request.make_response(
                json.dumps([]),
                headers=[('Content-Type', 'application/json')]
            )
        
    @http.route('/get_subtasks', type='http', auth='public', cors='*')
    def get_subtasks(self, **kwargs):
        try:
            subtasks = request.env['qctracker.subtask'].sudo().search([])
            subtask_list = []

            for sub in subtasks:
                subtask_data = {
                    'id':sub.id,
                    'name': sub.name,
                    'description': sub.description or "",
                    'task': sub.task_id.id if sub.task_id else "Aucune tâche",
                    'employee': sub.employee_id.name if sub.employee_id else "Inconnu",
                    'start_date': sub.start_date.isoformat() if sub.start_date else "",
                    'end_date': sub.end_date.isoformat() if sub.end_date else "",
                    'status': dict(sub._fields['status'].selection).get(sub.status, "Non défini")
                }
                subtask_list.append(subtask_data)

            return request.make_response(
                json.dumps(subtask_list),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des sous-tâches : {e}")
            return request.make_response(
                json.dumps([]),
                headers=[('Content-Type', 'application/json')]
            )
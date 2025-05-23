# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

"""
===== Objectif =====

Ce modèle représente un employé au sein de l'application Odoo. Il permet de gérer les informations relatives aux employés, telles que :

* Informations personnelles (nom, prénom, coordonnées)
* Informations professionnelles (rôle, département, compétences)
* Suivi des tâches et évaluations
* Gestion des notifications

===== Champs =====

* `name` (Char, calculé et stocké) : Nom complet de l'employé (calculé à partir des prénom et nom de famille).
* `first_name` (Char, obligatoire) : Prénom de l'employé.
* `last_name` (Char, obligatoire) : Nom de famille de l'employé.
* `email` (Char, obligatoire et unique) : Adresse e-mail de l'employé (format validé).
* `phone` (Char) : Numéro de téléphone de l'employé (format validé).
* `role` (Selection, obligatoire) : Rôle de l'employé (employé, manager, admin).
* `department_id` (Many2one vers `qctracker.department`) : Département auquel l'employé appartient.
* `is_manager` (Boolean, calculé et stocké) : Indique si l'employé est un manager (calculé à partir du rôle).
* `skill_ids` (Many2many vers `qctracker.skill`) : Compétences de l'employé.
* `task_ids` (One2many vers `qctracker.task`) : Tâches assignées à l'employé.
* `rating_employee_ids` (One2many vers `qctracker.employeerating`) : Évaluations de l'employé.
* `gender` (Selection) : Genre de l'employé.
* `country_id` (Many2one vers `res.country`) : Pays de l'employé (ID).
* `project_ids` (One2many vers `qctracker.project`) : Projets auxquels l'employé est associé.
* `user_id` (Many2one vers `res.users`) : Utilisateur Odoo associé à l'employé.
* `notification_ids` (One2many vers `qctracker.task.notification`) : Notifications associées à l'employé.
* `country_dynamic` (Selection) : Liste dynamique des pays (récupérée de `res.country`).
* `project_delivery_ids` (One2many vers `qctracker.projectdelivery`) : Livraisons de projet associées à l'employé.

===== Méthodes =====

* `_compute_full_name()` : Calcule le nom complet de l'employé en combinant le prénom et le nom de famille.
* `_compute_is_manager()` : Détermine si l'employé est un manager en fonction de son rôle.
* `_get_country_selection()` : Récupère la liste des pays disponibles pour la sélection dynamique.
* `_check_email()` : Valide le format de l'adresse e-mail de l'employé.
* `_check_phone()` : Valide le format du numéro de téléphone de l'employé.

===== Fonctionnalités Clés =====

* Gestion complète des informations des employés.
* Association des employés aux départements, projets et tâches.
* Suivi des compétences et des évaluations des employés.
* Validation des coordonnées (e-mail, téléphone).
* Gestion des notifications pour les employés.

===== Utilisation =====

Ce modèle est essentiel pour la gestion des employés dans l'application Odoo. Il centralise les informations des employés et facilite la gestion des ressources humaines.
"""


# --- QCTrackerEmployee Model ---
class QCTrackerEmployee(models.Model):
    """
    Modèle Odoo représentant un employé.
    Un employé peut appartenir à un département, être un manager et avoir des compétences.
    """
    _name = 'qctracker.employee'
    _description = 'Un employé peut appartenir à un département et être un manager'

    name = fields.Char(string='Nom Complet', compute='_compute_full_name', store=True)
    first_name = fields.Char(string='Prénom', required=True, size=256)
    last_name = fields.Char(string='Nom de Famille', required=True, size=256)
    email = fields.Char(string='Email', required=True, unique=True, widget="email")
    phone = fields.Char(string='Téléphone', size=32, widget="phone")
    role = fields.Selection([
        ('employee', 'Employé'),
        ('manager', 'Manager'),
        ('admin', 'Administrateur')
    ], string='Rôle', required=True)
    department_id = fields.Many2one('qctracker.department', string='Département')
    is_manager = fields.Boolean(string='Est Manager', compute='_compute_is_manager', store=True)

    task_ids = fields.One2many('qctracker.task', 'employee_id', string='Tâches Assignées',required=True)
    rating_employee_ids = fields.One2many('qctracker.employeerating', 'employee_id', 'Évaluations')
    skill_rating_ids = fields.One2many('qctracker.skillrating', 'employee_id', string='Évaluations de Compétences',required=True)
    gender = fields.Selection([('male', 'Homme'), ('female', 'Femme')], string='Genre')
    country_id = fields.Many2one(
    'res.country',
    string='Pays',
    domain="[('name', 'in', ['Cameroon', 'Senegal', 'Nigeria', 'Togo', 'Côte d'Ivoire', 'Mauritius'])]"
)

    project_ids = fields.One2many('qctracker.project', 'employee_id', string='Projets')
    user_id = fields.Many2one('res.users', string='Utilisateur Associé')
    project_delivery_ids = fields.One2many('qctracker.projectdelivery', 'employee_id', string='Livraisons de Projet')

    notification_ids = fields.One2many('qctracker.task.notification', 'recipient_id', string='Notifications')

    country_dynamic = fields.Selection(
        '_get_country_selection', string='Pays (Dynamique)',
        help='Sélectionnez un pays (liste dynamique)')

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        """
        Calcule le nom complet de l'employé en combinant le prénom et le nom de famille.
        """
        for rec in self:
            rec.name = f"{rec.first_name} {rec.last_name}" if rec.first_name and rec.last_name else ''

    @api.depends('role')
    def _compute_is_manager(self):
        """
        Détermine si l'employé est un manager en fonction de son rôle.
        """
        for rec in self:
            rec.is_manager = rec.role == 'manager'

    @api.model
    def _get_country_selection(self):
        """
        Récupère la liste des pays disponibles pour la sélection dynamique.
        """
        countries = self.env['res.country'].search([])
        return [(str(country.id), country.name) for country in sorted(countries, key=lambda country: country.name)]

    @api.constrains('email')
    def _check_email(self):
        """
        Valide l'adresse e-mail de l'employé en utilisant une expression régulière.
        """
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Adresse e-mail invalide.")

    @api.constrains('phone')
    def _check_phone(self):
        """
        Valide le numéro de téléphone de l'employé.
        """
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError("Numéro de téléphone invalide. Seuls les chiffres sont autorisés.")

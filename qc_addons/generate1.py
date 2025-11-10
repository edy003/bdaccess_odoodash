# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
import random
from odoo import api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WorkProgramDataGenerator(models.Model):
    _name = 'work.program.data.generator'
    _description = 'Générateur de données pour Work Programs'

    @api.model
    def generate_work_programs(self, months_past=6, months_future=6, programs_per_month=5):
        """
        Point d'entrée principal pour générer les WorkPrograms
        
        :param months_past: Nombre de mois dans le passé (défaut: 6)
        :param months_future: Nombre de mois dans le futur (défaut: 6)
        :param programs_per_month: Nombre de programmes par mois et par département (défaut: 5)
        """
        _logger.info("=== DÉBUT GÉNÉRATION WORK PROGRAMS ===")
        
        try:
            # Validation des prérequis
            if not self._validate_prerequisites():
                raise UserError("Données de base manquantes. Vérifiez les départements, employés, projets et workflows.")
            
            # Récupération des données de base
            base_data = self._get_base_data()
            
            # Génération des programmes
            programs_created = self._generate_programs_for_period(
                base_data, 
                months_past, 
                months_future, 
                programs_per_month
            )
            
            self.env.cr.commit()
            
            _logger.info(f"=== GÉNÉRATION TERMINÉE: {programs_created} programmes créés ===")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Succès',
                    'message': f'{programs_created} programmes de travail générés avec succès !',
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            _logger.error(f"ERREUR GÉNÉRATION: {e}", exc_info=True)
            self.env.cr.rollback()
            raise UserError(f"Erreur lors de la génération: {str(e)}")

    @api.model
    def _validate_prerequisites(self):
        """Vérifie que toutes les données nécessaires existent"""
        validations = {
            'hr.department': "Aucun département trouvé",
            'hr.employee': "Aucun employé trouvé",
            'workflow.activity': "Aucune activité workflow trouvée",
            'practice.practice': "Aucune pratique trouvée",
        }
        
        for model, error_msg in validations.items():
            if not self.env[model].search_count([]):
                _logger.error(error_msg)
                return False
        
        return True

    @api.model
    def _get_base_data(self):
        """Récupère et organise toutes les données nécessaires"""
        
        # Départements par type (internal/external)
        internal_depts = self.env['hr.department'].search([('dpt_type', '=', 'internal')])
        external_depts = self.env['hr.department'].search([('dpt_type', '=', 'external')])
        
        # Employés par département
        all_employees = self.env['hr.employee'].search([])
        internal_employees = [emp for emp in all_employees if emp.department_id.dpt_type == 'internal']
        external_employees = [emp for emp in all_employees if emp.department_id.dpt_type == 'external']
        
        # Practices par type
        consulting_practices = self.env['practice.practice'].search([('type', '=', 'consulting')])
        technology_practices = self.env['practice.practice'].search([('type', '=', 'technology')])
        
        # Activités par domaine
        all_activities = self.env['workflow.activity'].search([])
        internal_activities = []
        external_activities = []
        
        for activity in all_activities:
            activity_name = activity.name or ''
            # Activités INTERNES: contiennent PS4 ou PR5
            if 'PS4' in activity_name or 'PR5' in activity_name:
                internal_activities.append(activity)
            # Activités EXTERNES: contiennent PR1 ou PR2
            elif 'PR1' in activity_name or 'PR2' in activity_name:
                external_activities.append(activity)
        
        # === CRÉATION DES PROJETS ===
        internal_projects = self._create_internal_projects(internal_depts)
        external_projects = self._create_external_projects(external_depts, consulting_practices, technology_practices)
        
        _logger.info(f"Données chargées: {len(internal_employees)} employés internes, "
                    f"{len(external_employees)} employés externes, "
                    f"{len(internal_projects)} projets internes créés, "
                    f"{len(external_projects)} projets externes créés, "
                    f"{len(consulting_practices)} practices consulting, "
                    f"{len(technology_practices)} practices technology, "
                    f"{len(internal_activities)} activités internes, "
                    f"{len(external_activities)} activités externes")
        
        return {
            'internal_depts': internal_depts,
            'external_depts': external_depts,
            'internal_employees': internal_employees,
            'external_employees': external_employees,
            'internal_projects': internal_projects,
            'external_projects': external_projects,
            'consulting_practices': consulting_practices,
            'technology_practices': technology_practices,
            'internal_activities': internal_activities,
            'external_activities': external_activities,
        }

    @api.model
    def _generate_programs_for_period(self, base_data, months_past, months_future, programs_per_month):
        """Génère les programmes pour toute la période"""
        
        WorkProgram = self.env['work.program']
        programs_created = 0
        
        # Date de référence: 10 octobre 2025
        base_date = datetime(2025, 10, 10)
        
        # Générer pour chaque mois
        for month_offset in range(-months_past, months_future + 1):
            month_start, month_end = self._calculate_month_boundaries(base_date, month_offset)
            
            # Programmes pour départements INTERNES
            if base_data['internal_depts'] and base_data['internal_employees'] and base_data['internal_activities']:
                for dept in base_data['internal_depts']:
                    dept_employees = [emp for emp in base_data['internal_employees'] if emp.department_id.id == dept.id]
                    
                    if not dept_employees:
                        continue
                    
                    for _ in range(programs_per_month):
                        program_data = self._generate_single_program(
                            dept_employees,
                            base_data['internal_projects'],
                            base_data['internal_activities'],
                            dept,
                            month_start,
                            month_end,
                            is_external=False,
                            practices=[]
                        )
                        
                        if program_data:
                            try:
                                WorkProgram.create(program_data)
                                programs_created += 1
                            except Exception as e:
                                _logger.error(f"Erreur création programme interne: {e}")
            
            # Programmes pour départements EXTERNES
            if base_data['external_depts'] and base_data['external_employees'] and base_data['external_activities']:
                for dept in base_data['external_depts']:
                    dept_employees = [emp for emp in base_data['external_employees'] if emp.department_id.id == dept.id]
                    
                    if not dept_employees:
                        continue
                    
                    # Déterminer les practices appropriées pour ce département
                    # On cherche les practices qui ont ce département dans leurs department_ids
                    dept_practices = self.env['practice.practice'].search([
                        ('department_ids', 'in', [dept.id])
                    ])
                    
                    if not dept_practices:
                        # Fallback: utiliser toutes les practices
                        dept_practices = base_data['consulting_practices'] + base_data['technology_practices']
                    
                    for _ in range(programs_per_month):
                        program_data = self._generate_single_program(
                            dept_employees,
                            base_data['external_projects'],
                            base_data['external_activities'],
                            dept,
                            month_start,
                            month_end,
                            is_external=True,
                            practices=dept_practices
                        )
                        
                        if program_data:
                            try:
                                WorkProgram.create(program_data)
                                programs_created += 1
                            except Exception as e:
                                _logger.error(f"Erreur création programme externe: {e}")
        
        return programs_created

    @api.model
    def _calculate_month_boundaries(self, base_date, month_offset):
        """Calcule les dates de début et fin d'un mois"""
        year = base_date.year
        month = base_date.month + month_offset
        
        # Ajuster année si nécessaire
        while month <= 0:
            month += 12
            year -= 1
        while month > 12:
            month -= 12
            year += 1
        
        month_start = datetime(year, month, 1)
        
        # Calculer le dernier jour du mois
        if month == 12:
            next_month_start = datetime(year + 1, 1, 1)
        else:
            next_month_start = datetime(year, month + 1, 1)
        
        month_end = next_month_start - timedelta(days=1)
        
        return month_start, month_end

    @api.model
    def _generate_single_program(self, employees, projects, activities, department, 
                                 month_start, month_end, is_external=False, practices=None):
        """Génère un programme de travail individuel"""
        
        try:
            # Sélections aléatoires
            employee = random.choice(employees)
            activity = random.choice(activities)
            
            # Pour les projets externes, on filtre selon la practice
            if is_external and practices:
                # Sélectionner une practice aléatoire
                practice = random.choice(practices)
                
                # Filtrer les projets qui ont cette practice
                filtered_projects = [p for p in projects if p.practice_id and p.practice_id.id == practice.id]
                
                if not filtered_projects:
                    # Si aucun projet n'a cette practice, en assigner une au hasard
                    project = random.choice(projects)
                    # Optionnel: mettre à jour le projet avec cette practice
                    # project.write({'practice_id': practice.id})
                else:
                    project = random.choice(filtered_projects)
            else:
                project = random.choice(projects)
            
            # Date d'assignation dans le mois
            day = random.randint(1, month_end.day)
            assignment_date = datetime(month_start.year, month_start.month, day)
            
            # Construire les données complètes
            return self._build_program_data(
                employee, 
                project, 
                activity, 
                department, 
                assignment_date,
                is_external
            )
            
        except Exception as e:
            _logger.error(f"Erreur génération programme: {e}")
            return None

    @api.model
    def _build_program_data(self, employee, project, activity, department, assignment_date, is_external=False):
        """Construit toutes les données d'un programme de travail"""
        
        # === CALCULS TEMPORELS ===
        initial_deadline = assignment_date + timedelta(days=random.randint(7, 28))
        
        # État réaliste selon ancienneté
        state = self._get_state_by_age(assignment_date)
        
        # Reports possibles pour états avancés
        nb_postpones = 0
        actual_deadline = initial_deadline
        
        if state in ['ongoing', 'to_validate', 'validated', 'to_redo', 'done'] and random.random() < 0.35:
            nb_postpones = random.randint(1, 3)
            actual_deadline = initial_deadline + timedelta(days=nb_postpones * random.randint(3, 7))
        
        # === MÉTRIQUES SELON ÉTAT ===
        completion_percentage = self._get_completion_by_state(state)
        satisfaction_level = self._get_satisfaction_by_state(state)
        comments = self._generate_comments(state, activity.name, department.name)
        
        # === RELATIONS WORKFLOW ===
        procedure = self.env['workflow.procedure'].search([('activity_id', '=', activity.id)], limit=1)
        
        task_description = False
        if procedure:
            task_description = self.env['workflow.task.formulation'].search(
                [('procedure_id', '=', procedure.id)], 
                limit=1
            )
        
        # Livrables (1 à 3 max)
        deliverables = self.env['workflow.deliverable'].search([('activity_id', '=', activity.id)])
        deliverable_ids = False
        if deliverables:
            nb_deliverables = random.randint(1, min(3, len(deliverables)))
            selected_deliverables = random.sample(deliverables.ids, nb_deliverables)
            deliverable_ids = [(6, 0, selected_deliverables)]
        
        # === COLLABORATEURS SUPPORT ===
        dept_type = department.dpt_type
        support_pool = self.env['hr.employee'].search([
            ('department_id.dpt_type', '=', dept_type),
            ('id', '!=', employee.id)
        ])
        
        support_ids = False
        if support_pool:
            # Entre 0 et 3 collaborateurs support
            nb_support = random.randint(0, min(3, len(support_pool)))
            if nb_support > 0:
                selected_support = random.sample(support_pool.ids, nb_support)
                support_ids = [(6, 0, selected_support)]
        
        # === INPUTS ET DESCRIPTIONS ===
        inputs_needed = self._generate_inputs(activity.name, department.name)
        
        # === EFFORT SELON TYPE ===
        if is_external:
            # Projets externes: plus d'effort (consulting/technology)
            base_effort = random.choice([8, 16, 24, 32, 40, 56, 72])
        else:
            # Projets internes: moins d'effort (support)
            base_effort = random.choice([4, 8, 12, 16, 24, 32])
        
        duration_effort = base_effort + random.randint(-4, 8)
        
        # === NOM DU PROGRAMME ===
        month_name = self._get_month_name(assignment_date)
        week_number = assignment_date.isocalendar()[1]
        monday_str = self._get_monday_str(assignment_date)
        
        # Inclure la practice dans le nom pour projets externes
        if is_external and project.practice_id:
            practice_code = project.practice_id.sic or project.practice_id.name[:3].upper()
            program_name = (f"{practice_code}-"
                           f"{project.name[:12]}-"
                           f"{activity.name[:20]}-"
                           f"S{week_number:02d}")
        else:
            program_name = (f"{department.name[:3].upper()}-"
                           f"{project.name[:12]}-"
                           f"{activity.name[:20]}-"
                           f"S{week_number:02d}")
        
        # === CONSTRUCTION DU DICTIONNAIRE FINAL ===
        program_dict = {
            'name': program_name,
            'my_month': month_name,
            'week_of': week_number,
            'my_week_of': monday_str,
            
            # Relations
            'project_id': project.id,
            'activity_id': activity.id,
            'procedure_id': procedure.id if procedure else False,
            'task_description_id': task_description.id if task_description else False,
            'deliverable_ids': deliverable_ids,
            'support_ids': support_ids,
            'work_programm_department_id': department.id,
            'responsible_id': employee.id,
            
            # Caractéristiques
            'priority': random.choice(['low', 'medium', 'high']),
            'complexity': random.choice(['low', 'medium', 'high']),
            'duration_effort': duration_effort,
            
            # Dates
            'assignment_date': assignment_date.date(),
            'initial_deadline': initial_deadline.date(),
            'actual_deadline': actual_deadline.date(),
            'nb_postpones': nb_postpones,
            
            # État et progression
            'state': state,
            'completion_percentage': completion_percentage,
            'satisfaction_level': satisfaction_level,
            
            # Descriptions
            'inputs_needed': inputs_needed,
            'comments': comments,
        }
        
        # === CHAMPS EXTERNES (si applicable) ===
        if is_external:
            program_dict['champ1'] = f"Practice: {project.practice_id.name if project.practice_id else 'N/A'}"
            program_dict['champ2'] = f"Type: {project.practice_id.type if project.practice_id else 'N/A'} | Mission: {activity.name[:40]}"
        else:
            program_dict['champ1'] = ''
            program_dict['champ2'] = ''
        
        return program_dict

    # =========================================================================
    # MÉTHODES DE GÉNÉRATION INTELLIGENTE
    # =========================================================================

    @api.model
    def _get_state_by_age(self, assignment_date):
        """Détermine un état réaliste selon l'ancienneté de la tâche"""
        today = datetime.now().date()
        days_ago = (today - assignment_date.date()).days
        
        if days_ago < 0:  # Futur
            return 'draft'
        elif days_ago <= 2:
            return random.choices(['draft', 'ongoing'], weights=[30, 70])[0]
        elif days_ago <= 5:
            return random.choices(['draft', 'ongoing', 'to_validate'], weights=[10, 75, 15])[0]
        elif days_ago <= 10:
            return random.choices(
                ['ongoing', 'to_validate', 'validated', 'to_redo'],
                weights=[55, 25, 15, 5]
            )[0]
        elif days_ago <= 15:
            return random.choices(
                ['ongoing', 'to_validate', 'validated', 'refused', 'to_redo', 'done'],
                weights=[30, 20, 15, 8, 12, 15]
            )[0]
        elif days_ago <= 25:
            return random.choices(
                ['to_validate', 'validated', 'refused', 'to_redo', 'incomplete', 'done', 'cancelled'],
                weights=[12, 18, 5, 10, 10, 40, 5]
            )[0]
        elif days_ago <= 40:
            return random.choices(
                ['validated', 'to_redo', 'incomplete', 'done', 'cancelled'],
                weights=[15, 5, 10, 65, 5]
            )[0]
        else:  # Ancien (40+ jours)
            return random.choices(
                ['validated', 'incomplete', 'done', 'cancelled'],
                weights=[10, 8, 75, 7]
            )[0]

    @api.model
    def _get_completion_by_state(self, state):
        """Pourcentage de complétion selon l'état"""
        completion_map = {
            'draft': random.randint(0, 10),
            'ongoing': random.randint(20, 80),
            'to_validate': random.randint(85, 99),
            'validated': 100,
            'refused': random.randint(70, 95),
            'to_redo': random.randint(50, 85),
            'incomplete': random.randint(30, 75),
            'done': 100,
            'cancelled': random.randint(5, 60)
        }
        return completion_map.get(state, 50)

    @api.model
    def _get_satisfaction_by_state(self, state):
        """Niveau de satisfaction selon l'état"""
        if state in ['draft', 'ongoing', 'to_validate']:
            return False
        elif state == 'done':
            return random.choices(['high', 'medium', 'low'], weights=[70, 25, 5])[0]
        elif state == 'validated':
            return random.choices(['high', 'medium', 'low'], weights=[60, 30, 10])[0]
        elif state in ['refused', 'to_redo']:
            return random.choices(['low', 'medium', 'high'], weights=[60, 30, 10])[0]
        elif state == 'incomplete':
            return random.choices(['low', 'medium'], weights=[65, 35])[0]
        else:  # cancelled
            return random.choice([False, 'low'])

    @api.model
    def _generate_comments(self, state, activity_name, dept_name):
        """Génère des commentaires contextuels"""
        
        comments_templates = {
            'draft': [
                "Programme planifié - En attente de démarrage",
                "Nouvellement créé - Ressources à allouer",
                "Initialisé - Briefing prévu prochainement"
            ],
            'ongoing': [
                f"Travail en cours sur {activity_name[:40]}",
                "Progression selon planning établi",
                "Avancement satisfaisant avec quelques ajustements mineurs",
                "Coordination active avec les parties prenantes"
            ],
            'to_validate': [
                "Livrable finalisé - En attente de validation hiérarchique",
                "Travail terminé - Soumis pour revue qualité",
                "Prêt pour validation formelle du responsable",
                "Documentation complétée - Approbation requise"
            ],
            'validated': [
                "Validé avec succès par le responsable",
                "Conformité confirmée - Tâche clôturée",
                "Validation obtenue - Standards respectés",
                "Approuvé formellement - Mission accomplie"
            ],
            'refused': [
                "Validation refusée - Corrections majeures nécessaires",
                "Non-conformité détectée - Reprise complète demandée",
                "Standards non atteints - Réajustements requis",
                "Refus motivé - Nouvelle soumission attendue"
            ],
            'to_redo': [
                "À reprendre suite feedbacks - Ajustements ciblés",
                "Corrections mineures à apporter avant revalidation",
                "Quelques points à revoir selon remarques",
                "Reprise partielle nécessaire"
            ],
            'incomplete': [
                "Travail suspendu - Attente informations complémentaires",
                "Bloqué par dépendance externe non résolue",
                "En pause temporaire - Réaffectation priorités",
                "Ressources manquantes pour finalisation"
            ],
            'done': [
                "Terminé avec succès - Objectifs atteints",
                f"Mission accomplie pour {dept_name}",
                "Clôturé satisfaisant - Livrable opérationnel",
                "Finalisé conformément aux attentes"
            ],
            'cancelled': [
                "Annulé suite changement stratégique",
                "Programme abandonné - Contexte modifié",
                "Annulation décidée par la direction",
                "Plus nécessaire suite réorganisation"
            ]
        }
        
        templates = comments_templates.get(state, ["Programme en cours"])
        return random.choice(templates)

    @api.model
    def _generate_inputs(self, activity_name, dept_name):
        """Génère des inputs réalistes selon l'activité"""
        
        support_inputs = {
            'PS4.1_A1': "Bon de commande, spécifications techniques, validation budgétaire",
            'PS4.1_A2': "Contrat de licence, liste utilisateurs, budget approuvé",
            'PS4.1_A3': "Documentation fabricant, prérequis système, accès administrateur",
            'PS4.2_A1': "Formulaire de compte, validation RH, politique sécurité SI",
            'PS4.2_A2': "Rapport incident, logs système, backup complet",
            'PR5.1_A1': "Cahier des charges, compétences requises, disponibilités ressources",
        }
        
        consulting_inputs = {
            'PR1.1_A1': "CV consultants, modèles corporate, photos professionnelles",
            'PR1.1_A3': "Profils experts, portfolio réalisations, certifications",
            'PR1.2_A1': "Fiches capitalisation, témoignages clients, métriques performance",
            'PR1.2_A2': "Rapports fin mission, feedback client, durée et budget",
            'PR2.1_A1': "Appel d'offres, contraintes temporelles, contexte client",
        }
        
        # Rechercher correspondance
        inputs_dict = support_inputs if 'PS' in activity_name or 'PR5' in activity_name else consulting_inputs
        
        for key, value in inputs_dict.items():
            if key in activity_name:
                return value
        
        # Fallback générique
        return "Spécifications requises, validation managériale, documentation de référence"

    # =========================================================================
    # UTILITAIRES
    # =========================================================================

    @api.model
    def _get_month_name(self, date_obj):
        """Retourne le nom du mois en français"""
        months = {
            1: 'janvier', 2: 'fevrier', 3: 'mars', 4: 'avril',
            5: 'mai', 6: 'juin', 7: 'juillet', 8: 'aout',
            9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'decembre'
        }
        return months.get(date_obj.month, 'janvier')

    @api.model
    def _get_monday_str(self, date_obj):
        """Retourne la date du lundi de la semaine au format YYYY-MM-DD"""
        monday = date_obj - timedelta(days=date_obj.weekday())
        return monday.strftime('%Y-%m-%d')

    # =========================================================================
    # CRÉATION DES PROJETS
    # =========================================================================

    # =========================================================================
    # CRÉATION DES PROJETS AMÉLIORÉE
    # =========================================================================

    @api.model
    def _create_internal_projects(self, internal_depts):
        """Crée des projets internes COMPLETS pour chaque département interne"""
        Project = self.env['project.project']
        created_projects = []
        
        # Récupérer les utilisateurs disponibles (non-share, actifs)
        available_users = self.env['res.users'].search([
            ('share', '=', False),
            ('active', '=', True),
            ('id', '!=', 1)  # Exclure OdooBot
        ])
        
        if not available_users:
            _logger.warning("Aucun utilisateur trouvé, utilisation de l'utilisateur admin")
            available_users = self.env['res.users'].browse(2)  # Admin par défaut
        
        # Récupérer les partners existants (clients/fournisseurs)
        available_partners = self.env['res.partner'].search([
            ('is_company', '=', True),
            ('active', '=', True)
        ])
        
        # Récupérer les tags existants
        available_tags = self.env['project.tags'].search([])
        
        internal_project_templates = [
            {
                'name': 'Infrastructure IT 2025',
                'desc': 'Mise à niveau infrastructure serveurs et réseau',
                'label_tasks': 'Tâche IT'
            },
            {
                'name': 'Migration Cloud',
                'desc': 'Migration progressive des serveurs vers infrastructure cloud',
                'label_tasks': 'Tâche Cloud'
            },
            {
                'name': 'Sécurité SI',
                'desc': 'Renforcement sécurité système d\'information',
                'label_tasks': 'Tâche Sécurité'
            },
            {
                'name': 'Support N1-N2',
                'desc': 'Support utilisateurs quotidien et maintenance',
                'label_tasks': 'Ticket Support'
            },
            {
                'name': 'Maintenance Applicative',
                'desc': 'Maintenance et évolution applications internes',
                'label_tasks': 'Tâche Maintenance'
            },
            {
                'name': 'Gestion Licences',
                'desc': 'Gestion et optimisation du parc logiciels',
                'label_tasks': 'Tâche Licence'
            },
            {
                'name': 'Backup & Recovery',
                'desc': 'Stratégie sauvegarde et plan de reprise d\'activité',
                'label_tasks': 'Tâche Backup'
            },
            {
                'name': 'Monitoring SI',
                'desc': 'Supervision infrastructure et applications',
                'label_tasks': 'Tâche Monitoring'
            },
        ]
        
        for dept in internal_depts:
            # Créer 2-3 projets par département interne
            nb_projects = random.randint(2, 3)
            selected_templates = random.sample(
                internal_project_templates, 
                min(nb_projects, len(internal_project_templates))
            )
            
            for template in selected_templates:
                project_name = f"{template['name']} - {dept.name}"
                
                # Vérifier si le projet existe déjà
                existing = Project.search([('name', '=', project_name)], limit=1)
                if existing:
                    created_projects.append(existing)
                    continue
                
                # Sélectionner Project Manager et Assistant aléatoires
                project_manager = random.choice(available_users)
                
                # Assistant différent du manager
                assistant_pool = available_users.filtered(lambda u: u.id != project_manager.id)
                project_assistant = random.choice(assistant_pool) if assistant_pool else False
                
                # Sélectionner 0-2 partners aléatoires
                partner_ids = []
                if available_partners:
                    nb_partners = random.randint(0, min(2, len(available_partners)))
                    if nb_partners > 0:
                        selected_partners = random.sample(available_partners.ids, nb_partners)
                        partner_ids = [(6, 0, selected_partners)]
                
                # Sélectionner 0-3 tags aléatoires
                tag_ids = []
                if available_tags:
                    nb_tags = random.randint(0, min(3, len(available_tags)))
                    if nb_tags > 0:
                        selected_tags = random.sample(available_tags.ids, nb_tags)
                        tag_ids = [(6, 0, selected_tags)]
                
                # Générer dates réalistes
                # Date de début: entre -6 mois et +3 mois
                days_offset = random.randint(-180, 90)
                date_start = datetime.now() + timedelta(days=days_offset)
                
                # Date de fin: entre 3 et 12 mois après le début
                duration_days = random.randint(90, 365)
                date_end = date_start + timedelta(days=duration_days)
                
                try:
                    project_data = {
                        'name': project_name,
                        'project_type': 'internal',
                        'test_department_ids': [(6, 0, [dept.id])],
                        'active': True,
                        
                        # Champs manquants ajoutés
                        'label_tasks': template['label_tasks'],
                        'user_id': project_manager.id,  # Project Manager
                        'description': template['desc'],
                        'date_start': date_start.date(),
                        'date': date_end.date(),
                    }
                    
                    # Ajouter le partner si disponible
                    if partner_ids:
                        project_data['partner_id'] = partner_ids[0][2][0]  # Premier partner
                    
                    # Ajouter les tags
                    if tag_ids:
                        project_data['tag_ids'] = tag_ids
                    
                    # Ajouter l'assistant (si le champ existe dans votre modèle)
                    if project_assistant and hasattr(Project, 'project_assistant_id'):
                        project_data['project_assistant_id'] = project_assistant.id
                    
                    project = Project.create(project_data)
                    created_projects.append(project)
                    _logger.info(f"✓ Projet interne créé: {project_name} (Manager: {project_manager.name})")
                    
                except Exception as e:
                    _logger.error(f"✗ Erreur création projet interne {project_name}: {e}")
        
        return created_projects

    @api.model
    def _create_external_projects(self, external_depts, consulting_practices, technology_practices):
        """Crée des projets externes COMPLETS avec practices et subcategories"""
        Project = self.env['project.project']
        created_projects = []
        
        # Récupérer les utilisateurs disponibles
        available_users = self.env['res.users'].search([
            ('share', '=', False),
            ('active', '=', True),
            ('id', '!=', 1)
        ])
        
        if not available_users:
            available_users = self.env['res.users'].browse(2)
        
        # Récupérer les partners existants
        available_partners = self.env['res.partner'].search([
            ('is_company', '=', True),
            ('active', '=', True)
        ])
        
        # Récupérer les tags existants
        available_tags = self.env['project.tags'].search([])
        
        # Templates de projets externes par practice avec subcategories
        project_templates_by_practice = {
            'Transformation Digitale': [
                {
                    'name': 'Digitalisation Processus Client A',
                    'desc': 'Optimisation et digitalisation des processus métier',
                    'label_tasks': 'Tâche Digitalisation',
                    'subcategory': 'Optimisation des Processus'
                },
                {
                    'name': 'Transformation Numérique Secteur Bancaire',
                    'desc': 'Transformation digitale complète du système bancaire',
                    'label_tasks': 'Tâche Transformation',
                    'subcategory': 'Optimisation des Processus'
                },
            ],
            'Performance Financière': [
                {
                    'name': 'Optimisation Trésorerie Client B',
                    'desc': 'Amélioration gestion trésorerie et reporting',
                    'label_tasks': 'Tâche Finance',
                    'subcategory': 'Reporting IFRS'
                },
                {
                    'name': 'Audit Financier Groupe C',
                    'desc': 'Audit complet conformité IFRS',
                    'label_tasks': 'Tâche Audit',
                    'subcategory': 'Reporting IFRS'
                },
            ],
            'Gestion du Changement': [
                {
                    'name': 'Accompagnement Fusion-Acquisition',
                    'desc': 'Conduite du changement post-fusion',
                    'label_tasks': 'Tâche Changement',
                    'subcategory': 'Upskilling & Recrutement'
                },
                {
                    'name': 'Conduite Changement ERP',
                    'desc': 'Formation et accompagnement déploiement ERP',
                    'label_tasks': 'Tâche Formation',
                    'subcategory': 'Upskilling & Recrutement'
                },
            ],
            'Conseil Réglementaire': [
                {
                    'name': 'Conformité RGPD Client D',
                    'desc': 'Mise en conformité totale RGPD',
                    'label_tasks': 'Tâche Conformité',
                    'subcategory': 'Conformité RGPD'
                },
                {
                    'name': 'Audit Conformité Fiscale',
                    'desc': 'Audit et mise en conformité fiscale',
                    'label_tasks': 'Tâche Audit',
                    'subcategory': 'Conformité RGPD'
                },
            ],
            'Stratégie RH': [
                {
                    'name': 'Refonte Politique RH',
                    'desc': 'Révision complète politiques RH',
                    'label_tasks': 'Tâche RH',
                    'subcategory': 'Évaluation des Postes'
                },
                {
                    'name': 'Gestion Talents & Leadership',
                    'desc': 'Programme développement leadership',
                    'label_tasks': 'Tâche Talent',
                    'subcategory': 'Évaluation des Postes'
                },
            ],
            'Développement Mobile': [
                {
                    'name': 'App Mobile Banking',
                    'desc': 'Développement application bancaire iOS/Android',
                    'label_tasks': 'Story Mobile',
                    'subcategory': 'Développement iOS/Android'
                },
                {
                    'name': 'Application E-commerce Multi-plateforme',
                    'desc': 'App e-commerce native iOS et Android',
                    'label_tasks': 'Story Mobile',
                    'subcategory': 'Développement iOS/Android'
                },
            ],
            'Cybersécurité & SOC': [
                {
                    'name': 'Mise en place SOC Client E',
                    'desc': 'Déploiement Security Operations Center',
                    'label_tasks': 'Tâche Sécurité',
                    'subcategory': 'Tests d\'Intrusion Avancés'
                },
                {
                    'name': 'Audit Sécurité Applicative',
                    'desc': 'Pentest et audit sécurité applications',
                    'label_tasks': 'Tâche Pentest',
                    'subcategory': 'Tests d\'Intrusion Avancés'
                },
            ],
            'IA et Machine Learning': [
                {
                    'name': 'Chatbot IA Service Client',
                    'desc': 'Développement chatbot ML pour support client',
                    'label_tasks': 'Story IA',
                    'subcategory': 'Modèles Prédictifs'
                },
                {
                    'name': 'Prédiction Churn ML',
                    'desc': 'Modèle prédictif rétention client',
                    'label_tasks': 'Story ML',
                    'subcategory': 'Modèles Prédictifs'
                },
            ],
            'Migration Cloud': [
                {
                    'name': 'Migration AWS Client F',
                    'desc': 'Migration infrastructure complète vers AWS',
                    'label_tasks': 'Tâche Cloud',
                    'subcategory': 'Architecture AWS/Azure'
                },
                {
                    'name': 'Hybrid Cloud Azure',
                    'desc': 'Architecture hybride on-premise/Azure',
                    'label_tasks': 'Tâche Cloud',
                    'subcategory': 'Architecture AWS/Azure'
                },
            ],
            'Data Analytics': [
                {
                    'name': 'Data Warehouse BI',
                    'desc': 'Construction datawarehouse et dashboards',
                    'label_tasks': 'Story BI',
                    'subcategory': 'Solutions de BI'
                },
                {
                    'name': 'Analytics Prédictif Ventes',
                    'desc': 'Plateforme analytics prédiction ventes',
                    'label_tasks': 'Story Analytics',
                    'subcategory': 'Solutions de BI'
                },
            ],
        }
        
        all_practices = list(consulting_practices) + list(technology_practices)
        
        for practice in all_practices:
            # Trouver les départements associés
            practice_depts = [dept for dept in external_depts if dept.id in practice.department_ids.ids]
            
            if not practice_depts:
                practice_depts = [random.choice(external_depts)] if external_depts else []
            
            if not practice_depts:
                continue
            
            # Récupérer les templates pour cette practice
            templates = project_templates_by_practice.get(
                practice.name, 
                [{
                    'name': f'Projet {practice.name} #{i}',
                    'desc': f'Mission {practice.name}',
                    'label_tasks': 'Tâche',
                    'subcategory': None
                } for i in range(1, 4)]
            )
            
            # Créer 2-3 projets par practice
            nb_projects = random.randint(2, min(3, len(templates)))
            selected_templates = random.sample(templates, nb_projects)
            
            for template in selected_templates:
                project_name = template['name']
                
                # Vérifier si existe déjà
                existing = Project.search([('name', '=', project_name)], limit=1)
                if existing:
                    if not existing.practice_id:
                        existing.write({'practice_id': practice.id})
                    created_projects.append(existing)
                    continue
                
                # Sélectionner département
                selected_dept = random.choice(practice_depts)
                
                # Sélectionner Manager et Assistant
                project_manager = random.choice(available_users)
                assistant_pool = available_users.filtered(lambda u: u.id != project_manager.id)
                project_assistant = random.choice(assistant_pool) if assistant_pool else False
                
                # Partners et tags
                partner_ids = []
                if available_partners:
                    nb_partners = random.randint(1, min(2, len(available_partners)))
                    selected_partners = random.sample(available_partners.ids, nb_partners)
                    partner_ids = [(6, 0, selected_partners)]
                
                tag_ids = []
                if available_tags:
                    nb_tags = random.randint(1, min(3, len(available_tags)))
                    selected_tags = random.sample(available_tags.ids, nb_tags)
                    tag_ids = [(6, 0, selected_tags)]
                
                # Dates
                days_offset = random.randint(-180, 90)
                date_start = datetime.now() + timedelta(days=days_offset)
                duration_days = random.randint(90, 365)
                date_end = date_start + timedelta(days=duration_days)
                
                # Rechercher la subcategory
                subcategory_id = False
                if template.get('subcategory'):
                    subcategory = self.env['practice.subcategory'].search([
                        ('name', '=', template['subcategory']),
                        ('practice_id', '=', practice.id)
                    ], limit=1)
                    if subcategory:
                        subcategory_id = subcategory.id
                
                try:
                    project_data = {
                        'name': project_name,
                        'project_type': 'external',
                        'practice_id': practice.id,
                        'test_department_ids': [(6, 0, [selected_dept.id])],
                        'active': True,
                        
                        # Champs complets
                        'label_tasks': template['label_tasks'],
                        'user_id': project_manager.id,
                        'description': template['desc'],
                        'date_start': date_start.date(),
                        'date': date_end.date(),
                    }
                    
                    # Subcategory (si le champ existe)
                    if subcategory_id and hasattr(Project, 'subcategory_id'):
                        project_data['subcategory_id'] = subcategory_id
                    
                    # Partner
                    if partner_ids:
                        project_data['partner_id'] = partner_ids[0][2][0]
                    
                    # Tags
                    if tag_ids:
                        project_data['tag_ids'] = tag_ids
                    
                    # Assistant
                    if project_assistant and hasattr(Project, 'project_assistant_id'):
                        project_data['project_assistant_id'] = project_assistant.id
                    
                    project = Project.create(project_data)
                    created_projects.append(project)
                    _logger.info(
                        f"✓ Projet externe créé: {project_name} "
                        f"(Practice: {practice.name}, Subcat: {template.get('subcategory', 'N/A')}, "
                        f"Manager: {project_manager.name})"
                    )
                    
                except Exception as e:
                    _logger.error(f"✗ Erreur création projet externe {project_name}: {e}")
        
        return created_projects
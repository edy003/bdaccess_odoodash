import logging
from datetime import datetime, timedelta
import random
from odoo import api, models

_logger = logging.getLogger(__name__)


class DataSeederV2(models.Model):
    _name = 'data.seeder.v2'
    _description = 'Générateur exhaustif de données avec workflow complet et inputs'

    @api.model
    def seed_all_test_data(self):
        """Point d'entrée principal pour générer toutes les données"""
        _logger.info("=== DÉBUT GÉNÉRATION DONNÉES EXHAUSTIVES V2 ===")
        try:
            # Créer les structures workflow pour SUPPORT et CONSULTING
            activities = self.create_complete_workflow_structures()

            # Générer des WorkPrograms exhaustifs avec workflow réaliste
            self.seed_comprehensive_work_programs_v2(activities)

            self.env.cr.commit()
            _logger.info("=== GÉNÉRATION TERMINÉE AVEC SUCCÈS ===")
            return {'status': 'success', 'message': 'Données exhaustives générées avec succès'}
        except Exception as e:
            _logger.error(f"ERREUR GÉNÉRALE: {e}")
            self.env.cr.rollback()
            raise

    @api.model
    def create_complete_workflow_structures(self):
        """Crée les structures workflow complètes pour SUPPORT et CONSULTING"""
        _logger.info("Création des structures workflow complètes...")

        # Vérifier que tous les modèles nécessaires existent
        models_to_check = [
            'workflow.domain', 'workflow.process', 'workflow.subprocess',
            'workflow.activity', 'workflow.procedure', 'workflow.task.formulation',
            'workflow.deliverable'
        ]
        missing_models = [m for m in models_to_check if m not in self.env]
        if missing_models:
            _logger.warning(f"Modèles workflow manquants: {missing_models}")
            return {}

        workflows_config = self._get_complete_workflows_config()
        created_activities = {}

        for domain_name, workflow_data in workflows_config.items():
            domain = self._create_or_get_domain(domain_name, workflow_data.get('type', 'internal'))

            for process_data in workflow_data['processes']:
                process = self._create_or_get_process(process_data['name'], domain.id)

                for subprocess_data in process_data.get('sub_processes', []):
                    subprocess = self._create_or_get_subprocess(subprocess_data['name'], process.id)

                    for activity_data in subprocess_data.get('activities', []):
                        activity = self._create_or_get_activity(activity_data['name'], subprocess.id)
                        created_activities[activity.name] = activity

                        # Créer les procédures
                        for procedure_name in activity_data.get('procedures', []):
                            procedure = self._create_or_get_procedure(procedure_name, activity.id)

                            # Créer les formulations de tâches pour cette procédure
                            for task_form in activity_data.get('task_formulations', []):
                                self._create_or_get_task_formulation(task_form, procedure.id)

                        # Créer les livrables
                        for deliverable_name in activity_data.get('deliverables', []):
                            self._create_or_get_deliverable(deliverable_name, activity.id)

        return created_activities

    @api.model
    def seed_comprehensive_work_programs_v2(self, activities):
        """Génère des WorkPrograms exhaustifs V2 avec workflow réaliste"""
        _logger.info("=== DÉBUT GÉNÉRATION WORK.PROGRAMS V2 AVEC WORKFLOW ===")

        WorkProgram = self.env['work.program']

        # Récupérer les données existantes
        projects = list(self.env['project.project'].search([]))
        employees = list(self.env['hr.employee'].search([]))
        support_dept = self.env['hr.department'].search([('name', '=', 'Support')], limit=1)
        consulting_dept = self.env['hr.department'].search([('name', '=', 'Consulting')], limit=1)

        if not projects or not employees:
            _logger.warning("Projets ou employés inexistants, génération annulée")
            return

        # Séparer les employés par département
        support_employees = [emp for emp in employees if emp.department_id == support_dept]
        consulting_employees = [emp for emp in employees if emp.department_id == consulting_dept]

        # Séparer les activités par domaine
        support_activities = [act for name, act in activities.items() if 'PS4' in name or 'PR5' in name]
        consulting_activities = [act for name, act in activities.items() if 'PR1' in name or 'PR2' in name]

        # Base date fixe pour cohérence (1er septembre 2024)
        base_date = datetime(2024, 9, 1)
        program_counter = 1

        # Générer pour les 6 derniers mois + 6 mois futurs
        for month_offset in range(-6, 7):  # -6 à +6 mois
            # Calcul précis du mois cible
            target_year = base_date.year
            target_month = base_date.month + month_offset

            # Ajuster année si nécessaire
            while target_month <= 0:
                target_month += 12
                target_year -= 1
            while target_month > 12:
                target_month -= 12
                target_year += 1

            # Date du premier jour du mois cible
            month_start = datetime(target_year, target_month, 1)

            # Calculer le dernier jour du mois
            if target_month == 12:
                next_month_start = datetime(target_year + 1, 1, 1)
            else:
                next_month_start = datetime(target_year, target_month + 1, 1)
            month_end = next_month_start - timedelta(days=1)

            # Générer 3-5 programmes par mois pour chaque département
            nb_programs_per_month = random.randint(3, 5)

            # Générer pour le département SUPPORT
            if support_employees and support_activities:
                for i in range(nb_programs_per_month):
                    employee = random.choice(support_employees)
                    project = random.choice(projects)
                    activity = random.choice(support_activities)

                    # Date d'assignation dans le mois cible
                    day_in_month = random.randint(1, month_end.day)
                    assignment_date = datetime(target_year, target_month, day_in_month)

                    program_data = self._generate_program_data_v2(
                        employee, project, activity, support_dept,
                        assignment_date, program_counter
                    )

                    try:
                        WorkProgram.create(program_data)
                        program_counter += 1
                    except Exception as e:
                        _logger.error(f"Erreur création WorkProgram SUPPORT {employee.name}: {e}")

            # Générer pour le département CONSULTING
            if consulting_employees and consulting_activities:
                for i in range(nb_programs_per_month):
                    employee = random.choice(consulting_employees)
                    project = random.choice(projects)
                    activity = random.choice(consulting_activities)

                    # Date d'assignation dans le mois cible
                    day_in_month = random.randint(1, month_end.day)
                    assignment_date = datetime(target_year, target_month, day_in_month)

                    program_data = self._generate_program_data_v2(
                        employee, project, activity, consulting_dept,
                        assignment_date, program_counter
                    )

                    try:
                        WorkProgram.create(program_data)
                        program_counter += 1
                    except Exception as e:
                        _logger.error(f"Erreur création WorkProgram CONSULTING {employee.name}: {e}")

        _logger.info(f"=== FIN GÉNÉRATION WORK.PROGRAMS V2 - {program_counter - 1} programmes créés ===")

    def _get_complete_workflows_config(self):
        """Configuration complète des workflows pour SUPPORT et CONSULTING"""
        return {
            'Support': {
                'type': 'internal',
                'processes': [
                    {
                        'name': 'PS4. Gestion du système d\'information',
                        'sub_processes': [
                            {
                                'name': 'PS4.1: Gérer le parc informatique et bureautique',
                                'activities': [
                                    {
                                        'name': 'PS4.1_A1: Gérer les entrées / sorties d\'équipements informatiques',
                                        'procedures': [
                                            'PS4.1_A1_P1: Identifier les besoins en equipement TIC',
                                            'PS4.1_A1_P2: Valider, transmettre le besoin en equipement TIC',
                                            'PS4.1_A1_P3: Acquerir les equipements TIC',
                                            'PS4.1_A1_P4: Mettre à disposition et suivre les equipements informatique'
                                        ],
                                        'deliverables': ['PS4.1_A1_L1: Registre des actifs informatiques'],
                                        'task_formulations': [
                                            'Identifier les besoins en equipement TIC et les references appropriées',
                                            'Valider et transmettre le besoin en equipement TIC',
                                            'Acquerir les equipements TIC',
                                            'Mettre à disposition et suivre les equipements informatique'
                                        ]
                                    },
                                    {
                                        'name': 'PS4.1_A2: Gérer les licences et les abonnements',
                                        'procedures': [
                                            'PS4.1_A2_P1: Identifier et soumettre le besoin en license',
                                            'PS4.1_A2_P2: Valider et transmettre le besoin en license',
                                            'PS4.1_A2_P3: Effectuer l\'abonnement ou l\'acquisition du service',
                                            'PS4.1_A2_P4: Suivre les licences et abonnements'
                                        ],
                                        'deliverables': ['PS4.1_A2_L2: Fiche de besoin de license / abonnement'],
                                        'task_formulations': [
                                            'Identifier et soumettre le besoin en license ou abonnement',
                                            'Valider et transmettre le besoin en license ou abonnement',
                                            'Effectuer l\'abonnement ou l\'acquisition du service',
                                            'Suivre les licences et abonnements'
                                        ]
                                    },
                                    {
                                        'name': 'PS4.1_A3: Installer un équipement ou Logiciel',
                                        'procedures': [
                                            'PS4.1_A3_P1: Installer les équipements et systèmes TIC'
                                        ],
                                        'deliverables': [
                                            'PS4.1_A3_L4: Guide d\'installation des equipements ou logiciel',
                                            'PS4.1_A3_L5: Fiche d\'utilisation des outils',
                                            'PS4.1_A3_L6: Requete de maintenance',
                                            'PS4.1_A3_L7: Fiche de suivi de maintenance'
                                        ],
                                        'task_formulations': [
                                            'Installer les équipements et systèmes TIC',
                                            'Configurer les logiciels et applications',
                                            'Tester le bon fonctionnement des installations'
                                        ]
                                    }
                                ]
                            },
                            {
                                'name': 'PS4.2: Gérer le système de Gestion de l\'entreprise',
                                'activities': [
                                    {
                                        'name': 'PS4.2_A1: Gérer les utilisateurs et leurs droits',
                                        'procedures': [
                                            'PS4.2_A1_P1: Créer et gérer les comptes utilisateurs',
                                            'PS4.2_A1_P2: Attribuer et modifier les droits d\'accès'
                                        ],
                                        'deliverables': [
                                            'PS4.2_A1_L1: Matrice des droits',
                                            'PS4.2_A1_L2: Fiche de l\'utilisateur'
                                        ],
                                        'task_formulations': [
                                            'Créer et configurer les comptes utilisateurs',
                                            'Définir et attribuer les droits d\'accès',
                                            'Maintenir la matrice des droits'
                                        ]
                                    },
                                    {
                                        'name': 'PS4.2_A2: Maintenir le système',
                                        'procedures': [
                                            'PS4.2_A2_P1: Effectuer la maintenance corrective',
                                            'PS4.2_A2_P2: Effectuer la maintenance évolutive'
                                        ],
                                        'deliverables': ['PS4.2_A2_L3: Rapport de maintenance'],
                                        'task_formulations': [
                                            'Diagnostiquer et corriger les dysfonctionnements',
                                            'Mettre à jour et améliorer le système',
                                            'Documenter les interventions de maintenance'
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'name': 'PR5. Gestion de la Capacité (Staffing)',
                        'sub_processes': [
                            {
                                'name': 'PR5.1: Etablir les contrats',
                                'activities': [
                                    {
                                        'name': 'PR5.1_A1: Estimer le temps d\'intervention',
                                        'procedures': [
                                            'PR5.1_A1_P1: Estimation temporelle et planification',
                                            'PR5.1_A1_P2: Validation du plan de ressources'
                                        ],
                                        'deliverables': ['PR5.1_A1_L1: Plan de ressources'],
                                        'task_formulations': [
                                            'Estimer le temps d\'intervention et préparer le plan',
                                            'Valider le plan de ressources',
                                            'Ajuster la planification selon les contraintes'
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            'Consulting': {
                'type': 'external',
                'processes': [
                    {
                        'name': 'PR1. Faire des propositions',
                        'sub_processes': [
                            {
                                'name': 'PR1.1: Gérer le référentiel des consultants',
                                'activities': [
                                    {
                                        'name': 'PR1.1_A1: Gérer le BOOK CV',
                                        'procedures': [
                                            'PR1.1_A1_P1: Collecte de CV',
                                            'PR1.1_A1_P2: Instruction de mise à jour du Book CV',
                                            'PR1.1_A1_P3: Mise à jour du Book CV'
                                        ],
                                        'deliverables': [
                                            'PR1.1_A1_L1: Modèles et Instructions CV (Français et anglais)',
                                            'PR1.1_A1_L2: BOOK CVs suivant différents modèles'
                                        ],
                                        'task_formulations': [
                                            'Collecter les CV',
                                            'Donner les instructions de mise à jour du Book CV',
                                            'Mettre à jour le Book CV (Insertion, Modification, Suppression)',
                                            'Faire la revue et validation du Book CV'
                                        ]
                                    },
                                    {
                                        'name': 'PR1.1_A3: Gérer le BOOK Personnas',
                                        'procedures': [
                                            'PR1.1_A3_P1: Instruction de mise à jour du Book Persona',
                                            'PR1.1_A3_P2: Mise à jour du Book Persona',
                                            'PR1.1_A3_P3: Revue et Validation du Book Persona'
                                        ],
                                        'deliverables': [
                                            'PR1.1_A2_L1: Modèle et Instructions Profile (Français et anglais)',
                                            'PR1.1_A5_L2: Dossier expert'
                                        ],
                                        'task_formulations': [
                                            'Donner les instructions de mise à jour du Book Persona',
                                            'Faire la mise à jour du Book Persona (Insertion, Modification, Suppression)',
                                            'Faire la revue et validation du Book Persona'
                                        ]
                                    }
                                ]
                            },
                            {
                                'name': 'PR1.2: Gérer les références/expériences',
                                'activities': [
                                    {
                                        'name': 'PR1.2_A1: Gérer le BOOK Références détaillés',
                                        'procedures': [
                                            'PR1.2_A1_P3: Mise à jour du Book Références',
                                            'PR1.2_A1_P4: Revue et Validation du Book Références'
                                        ],
                                        'deliverables': [
                                            'PR1.2_A1_L1: Modèles et Instructions Reference (Français et anglais)',
                                            'PR1.2_A1_L2: BOOK Références détaillés suivant différents modèles'
                                        ],
                                        'task_formulations': [
                                            'Mettre à jour le Book Références (Insertion, Modification, Suppression)',
                                            'Faire la revue et validation du Book Références'
                                        ]
                                    },
                                    {
                                        'name': 'PR1.2_A2: Gérer le registre des expériences',
                                        'procedures': [
                                            'PR1.2_A2_P1: Instruction de mise à jour du Registre des Expériences',
                                            'PR1.2_A2_P2: Mise à jour du Registre des expériences'
                                        ],
                                        'deliverables': [
                                            'PR1.2_A2_L1: Modèles et Instructions Registre des expériences',
                                            'PR1.2_A2_L2: Registre des expériences'
                                        ],
                                        'task_formulations': [
                                            'Donner les instructions de mise à jour du Registre des Expériences',
                                            'Mettre à jour le Registre des expériences (Insertion, Modification, Suppression)'
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'name': 'PR2. Préparation des Missions',
                        'sub_processes': [
                            {
                                'name': 'PR2.1: Elaborer le plan projet',
                                'activities': [
                                    {
                                        'name': 'PR2.1_A1: Définir la méthodologie projet',
                                        'procedures': [
                                            'PR2.1_A1_P1: Analyser les exigences du projet',
                                            'PR2.1_A1_P2: Sélectionner la méthodologie appropriée'
                                        ],
                                        'deliverables': ['PR2.1_A1_L1: Document de méthodologie projet'],
                                        'task_formulations': [
                                            'Analyser les exigences et contraintes du projet',
                                            'Sélectionner et adapter la méthodologie appropriée',
                                            'Documenter la méthodologie retenue'
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }

    def _create_or_get_domain(self, name, domain_type):
        """Crée ou récupère un domaine"""
        Domain = self.env['workflow.domain']
        domain = Domain.search([('name', '=', name)], limit=1)
        if not domain:
            domain = Domain.create({'name': name, 'dpt_type': domain_type})
        return domain

    def _create_or_get_process(self, name, domain_id):
        """Crée ou récupère un processus"""
        Process = self.env['workflow.process']
        process = Process.search([('name', '=', name)], limit=1)
        if not process:
            process = Process.create({'name': name, 'domain_id': domain_id})
        return process

    def _create_or_get_subprocess(self, name, process_id):
        """Crée ou récupère un sous-processus"""
        SubProcess = self.env['workflow.subprocess']
        subprocess = SubProcess.search([('name', '=', name)], limit=1)
        if not subprocess:
            subprocess = SubProcess.create({'name': name, 'process_id': process_id})
        return subprocess

    def _create_or_get_activity(self, name, subprocess_id):
        """Crée ou récupère une activité"""
        Activity = self.env['workflow.activity']
        activity = Activity.search([('name', '=', name)], limit=1)
        if not activity:
            activity = Activity.create({'name': name, 'sub_process_id': subprocess_id})
        return activity

    def _create_or_get_procedure(self, name, activity_id):
        """Crée ou récupère une procédure"""
        Procedure = self.env['workflow.procedure']
        procedure = Procedure.search([('name', '=', name)], limit=1)
        if not procedure:
            procedure = Procedure.create({'name': name, 'activity_id': activity_id})
        return procedure

    def _create_or_get_task_formulation(self, name, procedure_id):
        """Crée ou récupère une formulation de tâche"""
        TaskForm = self.env['workflow.task.formulation']
        task_form = TaskForm.search([('name', '=', name)], limit=1)
        if not task_form:
            task_form = TaskForm.create({'name': name, 'procedure_id': procedure_id})
        return task_form

    def _create_or_get_deliverable(self, name, activity_id):
        """Crée ou récupère un livrable"""
        Deliverable = self.env['workflow.deliverable']
        deliverable = Deliverable.search([('name', '=', name)], limit=1)
        if not deliverable:
            deliverable = Deliverable.create({'name': name, 'activity_id': activity_id})
        return deliverable

    def _get_month_name_from_date(self, date_obj):
        """Retourne le nom du mois en français à partir d'une date"""
        months_fr = {
            1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril',
            5: 'mai', 6: 'juin', 7: 'juillet', 8: 'août',
            9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
        }
        return months_fr.get(date_obj.month, 'janvier')

    def _get_week_of_year(self, date_obj):
        """Retourne le numéro de semaine dans l'année"""
        return date_obj.isocalendar()[1]

    def _get_monday_of_week(self, date_obj):
        """Retourne le lundi de la semaine pour une date donnée au format YYYY-MM-DD"""
        monday = date_obj - timedelta(days=date_obj.weekday())
        return monday.strftime("%Y-%m-%d")

    def _generate_realistic_inputs_needed(self, activity_name, department_name):
        """Génère des inputs réalistes selon l'activité et le département"""
        
        # Inputs pour département SUPPORT
        support_inputs = {
            'PS4.1_A1': [
                'Bon de commande validé, Spécifications techniques des équipements',
                'Fiche de demande matériel, Budget approuvé',
                'Cahier des charges TIC, Liste des fournisseurs agréés',
                'Inventaire actuel du parc, Besoins exprimés par les services'
            ],
            'PS4.1_A2': [
                'Contrat de licence existant, Budget alloué pour les licences',
                'Liste des utilisateurs nécessitant une licence, Validation hiérarchique',
                'Tableau de bord des licences expirées, Recommandations techniques',
                'Demande formelle du service, Conditions générales du fournisseur'
            ],
            'PS4.1_A3': [
                'Documentation technique du matériel, Prérequis système',
                'Guide d\'installation fourni par le fabricant, Accès administrateur',
                'Schéma réseau de l\'entreprise, Configurations de sécurité',
                'Checklist de validation, Environnement de test disponible'
            ],
            'PS4.2_A1': [
                'Formulaire de création de compte, Validation du responsable RH',
                'Matrice des rôles et responsabilités, Politique de sécurité SI',
                'Liste des applications accessibles, Profil type du poste',
                'Demande de modification d\'accès, Attestation de formation sécurité'
            ],
            'PS4.2_A2': [
                'Rapport d\'incident ou anomalie, Logs système détaillés',
                'Backup complet du système, Plan de reprise d\'activité',
                'Demande d\'évolution fonctionnelle, Analyse d\'impact',
                'Documentation technique du système, Environnement de test'
            ],
            'PR5.1_A1': [
                'Cahier des charges du projet, Compétences requises',
                'Planning prévisionnel des activités, Disponibilités des ressources',
                'Budget alloué au staffing, Contraintes client',
                'Historique des interventions similaires, Profils des consultants disponibles'
            ]
        }
        
        # Inputs pour département CONSULTING
        consulting_inputs = {
            'PR1.1_A1': [
                'CV des consultants format Word/PDF, Modèles de CV corporate',
                'Photos professionnelles des consultants, Certificats et diplômes',
                'Références clients à valoriser, Guidelines de présentation',
                'Historique des missions réalisées, Compétences techniques actualisées'
            ],
            'PR1.1_A3': [
                'Profils détaillés des experts, Portfolio de réalisations',
                'Domaines d\'expertise documentés, Testimonials clients',
                'Publications et articles, Certifications professionnelles',
                'Projets marquants avec résultats mesurables, Outils et méthodologies maîtrisés'
            ],
            'PR1.2_A1': [
                'Fiches de capitalisation de mission, Témoignages clients',
                'Métriques de performance projet, Contexte et enjeux client',
                'Solutions apportées documentées, Résultats obtenus chiffrés',
                'Coordonnées référents client (avec accord), Support visuel (slides, schémas)'
            ],
            'PR1.2_A2': [
                'Rapports de fin de mission, Feedback client formalisé',
                'Durée et budget des interventions, Équipe projet et rôles',
                'Technologies et outils utilisés, Difficultés rencontrées et solutions',
                'Livrables produits, Lessons learned documentées'
            ],
            'PR2.1_A1': [
                'Appel d\'offres ou brief client, Contraintes temporelles et budgétaires',
                'Contexte organisationnel du client, Niveau de maturité projet',
                'Frameworks méthodologiques disponibles (Agile, Waterfall, Hybrid)',
                'Ressources allouées au projet, Risques identifiés initialement'
            ]
        }
        
        # Sélectionner les inputs appropriés
        if department_name == 'Support':
            for key in support_inputs:
                if key in activity_name:
                    return random.choice(support_inputs[key])
            return 'Spécifications techniques, Validation managériale, Documentation existante'
        else:  # Consulting
            for key in consulting_inputs:
                if key in activity_name:
                    return random.choice(consulting_inputs[key])
            return 'Brief client, Documentation projet, Ressources all'

    def _get_realistic_state_distribution(self, assignment_date):
        """
        Détermine un état réaliste selon la date d'assignation - CORRECTION COMPLÈTE
        Distribution équilibrée sur TOUS les 9 états possibles
        """
        today = datetime.now().date()
        days_since_assignment = (today - assignment_date).days
        
        # TÂCHES FUTURES (non encore assignées)
        if days_since_assignment < 0:
            return 'draft'
        
        # JOUR 0-2 : Phase initiale (draft + début ongoing)
        elif days_since_assignment <= 2:
            return random.choices(
                ['draft', 'ongoing'],
                weights=[35, 65]
            )[0]
        
        # JOUR 3-5 : Démarrage (draft, ongoing, premiers to_validate)
        elif days_since_assignment <= 5:
            return random.choices(
                ['draft', 'ongoing', 'to_validate'],
                weights=[10, 75, 15]
            )[0]
        
        # JOUR 6-9 : Progression (ongoing dominant, validations commencent)
        elif days_since_assignment <= 9:
            return random.choices(
                ['draft', 'ongoing', 'to_validate', 'validated', 'incomplete'],
                weights=[5, 55, 25, 10, 5]
            )[0]
        
        # JOUR 10-14 : Validation active (apparition refused et to_redo)
        elif days_since_assignment <= 14:
            return random.choices(
                ['ongoing', 'to_validate', 'validated', 'refused', 'to_redo', 'incomplete', 'done'],
                weights=[30, 20, 15, 12, 10, 8, 5]
            )[0]
        
        # JOUR 15-21 : Cycles validation/refus (tous états sauf draft)
        elif days_since_assignment <= 21:
            return random.choices(
                ['ongoing', 'to_validate', 'validated', 'refused', 'to_redo', 'incomplete', 'done', 'cancelled'],
                weights=[18, 15, 15, 10, 12, 10, 17, 3]
            )[0]
        
        # JOUR 22-30 : Finalisation (done augmente, ongoing diminue)
        elif days_since_assignment <= 30:
            return random.choices(
                ['ongoing', 'to_validate', 'validated', 'refused', 'to_redo', 'incomplete', 'done', 'cancelled'],
                weights=[10, 10, 12, 5, 8, 12, 38, 5]
            )[0]
        
        # JOUR 31-45 : Majorité terminée
        elif days_since_assignment <= 45:
            return random.choices(
                ['to_validate', 'validated', 'to_redo', 'incomplete', 'done', 'cancelled'],
                weights=[8, 15, 5, 10, 55, 7]
            )[0]
        
        # JOUR 46-60 : Quasi finalisé
        elif days_since_assignment <= 60:
            return random.choices(
                ['validated', 'to_redo', 'incomplete', 'done', 'cancelled'],
                weights=[12, 3, 8, 70, 7]
            )[0]
        
        # JOUR 61+ : Anciennes tâches (done, validated, cancelled, incomplete)
        else:
            return random.choices(
                ['validated', 'incomplete', 'done', 'cancelled'],
                weights=[8, 7, 78, 7]
            )[0]

    def _get_completion_by_state(self, state):
        """
        Retourne un pourcentage de complétion réaliste selon l'état
        CORRECTION: Tous les 9 états gérés
        """
        completion_ranges = {
            'draft': (0, 15),           # Juste initié
            'ongoing': (20, 75),         # En progression variable
            'to_validate': (85, 98),     # Quasi terminé, en attente
            'validated': (95, 100),      # Validé = très avancé
            'refused': (70, 92),         # Travail fait mais non accepté
            'to_redo': (35, 70),         # Partiellement fait, à reprendre
            'incomplete': (25, 80),      # Variable selon raison d'arrêt
            'done': (98, 100),           # Complètement terminé
            'cancelled': (5, 65)         # Variable selon moment annulation
        }
        min_val, max_val = completion_ranges.get(state, (0, 100))
        return random.randint(min_val, max_val)

    def _get_satisfaction_by_state(self, state):
        """
        Retourne un niveau de satisfaction réaliste selon l'état
        CORRECTION: Tous les 9 états gérés avec logique appropriée
        """
        # États non terminés = pas de satisfaction (False)
        if state in ['draft', 'ongoing', 'to_validate']:
            return False
        
        # DONE : excellente satisfaction généralement
        elif state == 'done':
            return random.choices(
                ['high', 'medium', 'low'],
                weights=[70, 22, 8]
            )[0]
        
        # VALIDATED : bonne satisfaction
        elif state == 'validated':
            return random.choices(
                ['high', 'medium', 'low'],
                weights=[60, 30, 10]
            )[0]
        
        # REFUSED : satisfaction faible/moyenne
        elif state == 'refused':
            return random.choices(
                ['low', 'medium', 'high'],
                weights=[65, 30, 5]
            )[0]
        
        # TO_REDO : satisfaction moyenne/faible
        elif state == 'to_redo':
            return random.choices(
                ['low', 'medium', 'high'],
                weights=[50, 40, 10]
            )[0]
        
        # INCOMPLETE : satisfaction faible principalement
        elif state == 'incomplete':
            return random.choices(
                ['low', 'medium', False],
                weights=[55, 30, 15]
            )[0]
        
        # CANCELLED : variable ou absent
        elif state == 'cancelled':
            return random.choices(
                ['low', 'medium', False],
                weights=[35, 25, 40]
            )[0]
        
        # Fallback (ne devrait pas arriver)
        else:
            return False

    def _generate_realistic_comments(self, state, activity_name, department_name):
        """
        Génère des commentaires réalistes selon l'état et le contexte
        CORRECTION: Tous les 9 états avec commentaires spécifiques
        """
        
        support_comments = {
            'draft': [
                'Nouvelle tâche créée, en attente de ressources',
                'Analyse préliminaire des besoins à réaliser',
                'En attente de validation budgétaire avant démarrage',
                'Création de la demande d\'intervention',
                'Évaluation des prérequis techniques en cours'
            ],
            'ongoing': [
                f'Intervention technique en cours sur {activity_name}',
                'Traitement des demandes utilisateurs en progression',
                'Configuration et tests en cours de réalisation',
                'Coordination avec les équipes métier active',
                'Résolution des incidents techniques identifiés',
                'Déploiement progressif en environnement de test'
            ],
            'to_validate': [
                'Travail terminé, soumis pour validation managériale',
                'Tests finalisés avec succès, en attente revue qualité',
                'Documentation technique complétée et transmise',
                'Intervention terminée, vérification conformité en cours',
                'Livraison effectuée, approbation formelle attendue'
            ],
            'validated': [
                'Travail validé par le responsable, documentation archivée',
                'Validation obtenue, mise en production planifiée',
                'Tâche validée et clôturée avec succès',
                'Conformité confirmée, passage en production autorisé',
                'Approbation formelle reçue, tâche finalisée'
            ],
            'refused': [
                'Validation refusée - Non-conformité standards détectée',
                'Retour arrière nécessaire suite revue qualité négative',
                'Corrections majeures exigées par le validateur',
                'Tests validation échoués, reprise complète demandée',
                'Écart significatif vs spécifications identifié'
            ],
            'to_redo': [
                'Reprise nécessaire suite feedbacks techniques',
                'Ajustements importants demandés par le manager',
                'Refonte partielle requise pour conformité normes',
                'Corrections à apporter suite refus validation',
                'Réajustement technique exigé après tests'
            ],
            'incomplete': [
                'Tâche suspendue - Attente informations complémentaires',
                'Bloqué par dépendance externe non résolue',
                'Mise en pause temporaire - Réaffectation priorités',
                'Ressources insuffisantes pour finalisation',
                'En attente matériel/logiciel manquant critique',
                'Suspendu suite changement périmètre projet'
            ],
            'done': [
                'Tâche finalisée avec succès, en production',
                'Intervention complétée, utilisateurs formés',
                'Clôture complète - Satisfaction confirmée',
                'Déploiement réussi, monitoring actif',
                'Objectifs atteints, documentation livrée'
            ],
            'cancelled': [
                'Annulé suite changement priorités organisationnelles',
                'Projet abandonné par décision direction',
                'Tâche obsolète suite évolution contexte',
                'Annulation pour raisons budgétaires',
                'Dépriorisation suite réorganisation interne'
            ]
        }
        
        consulting_comments = {
            'draft': [
                'Préparation proposition commerciale en cours',
                'Analyse du brief client initiée',
                'Constitution équipe projet à finaliser',
                'Cadrage initial avec sponsor planifié',
                'Définition périmètre intervention en discussion'
            ],
            'ongoing': [
                f'Mission {activity_name} en cours de réalisation',
                'Phase collecte données et analyse active',
                'Ateliers collaboratifs client en cours',
                'Développement livrables selon planning',
                'Interviews parties prenantes programmées',
                'Analyse processus métier client approfondie'
            ],
            'to_validate': [
                'Livrables finaux soumis client pour validation',
                'Présentation résultats effectuée, feedback attendu',
                'Revue qualité interne OK, soumission client',
                'Draft final transmis pour approbation formelle',
                'Comité pilotage validation prévu cette semaine'
            ],
            'validated': [
                'Livrables validés par client - Mission réussie',
                'Validation formelle obtenue, facturation lancée',
                'Succès confirmé, étude de cas documentée',
                'Acceptation client formalisée par PV recette',
                'Validation sponsor acquise, clôture administrative'
            ],
            'refused': [
                'Proposition refusée - Réorientation nécessaire',
                'Livrables non conformes attentes client',
                'Validation refusée, modifications majeures requises',
                'Client demande révision complète approche',
                'Écart significatif vs cahier charges identifié'
            ],
            'to_redo': [
                'Reprise complète suite feedbacks client négatifs',
                'Réajustement approche méthodologique exigé',
                'Nouvelle itération demandée par sponsor',
                'Révision recommandations selon nouvelles contraintes',
                'Refonte livrables pour conformité demandée'
            ],
            'incomplete': [
                'Mission suspendue - Attente décision stratégique client',
                'Bloqué par contraintes organisationnelles client',
                'Mise en pause temporaire, budget gelé',
                'Données critiques manquantes côté client',
                'Attente validation hypothèses travail',
                'Suspendu suite réorganisation majeure client'
            ],
            'done': [
                'Mission finalisée succès total - Client très satisfait',
                'Tous livrables acceptés, recommandation obtenue',
                'Clôture projet - ROI démontré formellement',
                'Objectifs largement dépassés, extension discutée',
                'Succès complet, témoignage client formalisé'
            ],
            'cancelled': [
                'Projet annulé client - Changement stratégique majeur',
                'Mission abandonnée suite réorganisation client',
                'Annulation contractuelle - Contexte économique',
                'Arrêt suite fusion/acquisition chez client',
                'Projet stoppé, priorités client redéfinies'
            ]
        }
        
        # Sélectionner commentaires appropriés
        if department_name == 'Support':
            comments_list = support_comments.get(state, support_comments['ongoing'])
        else:  # Consulting
            comments_list = consulting_comments.get(state, consulting_comments['ongoing'])
        
        return random.choice(comments_list)

    def _generate_program_data_v2(self, employee, project, activity, department, assignment_date, counter):
        """
        Génère les données réalistes pour un WorkProgram V2
        CORRECTION: Utilisation des fonctions corrigées pour tous les états
        """
        
        # Calculs dates et semaines
        month_name = self._get_month_name_from_date(assignment_date)
        week_of_year = self._get_week_of_year(assignment_date)
        monday_of_week = self._get_monday_of_week(assignment_date)
        initial_deadline = assignment_date + timedelta(days=random.randint(7, 28))

        # ÉTAT RÉALISTE avec distribution correcte sur 9 états
        state = self._get_realistic_state_distribution(assignment_date.date())

        # Gestion reports et deadlines selon état
        nb_postpones = 0
        actual_deadline = initial_deadline
        
        # Reports possibles pour états avancés
        if state in ['ongoing', 'to_validate', 'validated', 'to_redo', 'done'] and random.random() < 0.35:
            nb_postpones = random.randint(1, 3)
            actual_deadline = initial_deadline + timedelta(days=nb_postpones * random.randint(3, 7))

        # COMPLÉTION selon état (fonction corrigée)
        completion_percentage = self._get_completion_by_state(state)

        # Efforts variables
        if department.name == 'Support':
            base_effort = random.choice([4, 8, 12, 16, 24])
        else:  # Consulting
            base_effort = random.choice([8, 16, 24, 32, 40, 56])

        # Relations workflow
        procedures = self.env['workflow.procedure'].search([('activity_id', '=', activity.id)])
        procedure_id = procedures[0].id if procedures else False

        task_formulation_id = False
        if procedure_id:
            task_formulations = self.env['workflow.task.formulation'].search([('procedure_id', '=', procedure_id)])
            task_formulation_id = task_formulations[0].id if task_formulations else False

        deliverables = self.env['workflow.deliverable'].search([('activity_id', '=', activity.id)])
        deliverable_ids = [(6, 0, [d.id for d in deliverables[:random.randint(1, min(3, len(deliverables)))]])] if deliverables else [(5, 0, 0)]

        # Support
        potential_support = [emp for emp in self.env['hr.employee'].search([('department_id', '=', department.id)])
                             if emp.id != employee.id]
        nb_support = random.randint(0, min(2, len(potential_support)))
        support_ids = [(6, 0, [emp.id for emp in random.sample(potential_support, nb_support)])] if potential_support else [(5, 0, 0)]

        # Inputs réalistes
        inputs_needed = self._generate_realistic_inputs_needed(activity.name, department.name)

        # SATISFACTION selon état (fonction corrigée)
        satisfaction_level = self._get_satisfaction_by_state(state)

        # COMMENTAIRES selon état (fonction corrigée)
        comments = self._generate_realistic_comments(state, activity.name, department.name)

        program_data = {
            'name': f'{department.name}-{counter:03d}-{project.name[:15]}-{month_name}',
            'my_month': month_name,
            'week_of': week_of_year,
            'my_week_of': monday_of_week,
            'project_id': project.id,
            'activity_id': activity.id,
            'procedure_id': procedure_id,
            'task_description_id': task_formulation_id,
            'inputs_needed': inputs_needed,
            'deliverable_ids': deliverable_ids,
            'support_ids': support_ids,
            'work_programm_department_id': department.id,
            'priority': random.choice(['low', 'medium', 'high']),
            'complexity': random.choice(['low', 'medium', 'high']),
            'duration_effort': base_effort + random.randint(-4, 8),
            'state': state,  # État parmi les 9 possibles
            'completion_percentage': completion_percentage,
            'assignment_date': assignment_date.date(),
            'initial_deadline': initial_deadline.date(),
            'actual_deadline': actual_deadline.date(),
            'nb_postpones': nb_postpones,
            'responsible_id': employee.id,
            'satisfaction_level': satisfaction_level,
            'comments': comments,
            'champ1': f"Données spécifiques {department.name}" if department.dpt_type == 'external' else '',
            'champ2': f"Informations complémentaires mission {counter}" if department.dpt_type == 'external' else ''
        }

        return program_data
import factory
import random
from datetime import date, timedelta
from factory.fuzzy import FuzzyDate, FuzzyFloat, FuzzyChoice, FuzzyInteger
from collections import defaultdict



# Définition des modèles Factory pour toutes les entités
# Structure JSON complète et imbriquée des départements, catégories, compétences et projets
COMPANY_DATA = {
    "SOLUTION": {
        "name": "SOLUTION",
        "skill_categories": {
            "Développement logiciel": {
                "skills": [
                    "Software Development", "Web Development", "Mobile Development", 
                    "API Development", "Full-Stack Development"
                ]
            },
            "Architecture IT": {
                "skills": [
                    "System Integration", "Solution Architecture", "Enterprise Architecture", 
                    "Technical Design", "Microservices Architecture"
                ]
            },
            "Cloud Computing": {
                "skills": [
                    "Cloud Architecture", "Cloud Migration", "AWS", "Azure", 
                    "Google Cloud Platform", "Multi-Cloud Strategy"
                ]
            },
            "Données": {
                "skills": [
                    "Big Data", "Data Engineering", "Data Science", 
                    "Data Visualization", "Business Intelligence", "ETL Processes"
                ]
            },
            "Intelligence artificielle": {
                "skills": [
                    "AI Research", "Machine Learning", "Natural Language Processing", 
                    "Computer Vision", "Deep Learning"
                ]
            },
            "Gestion de données": {
                "skills": [
                    "Database Management", "SQL", "NoSQL", "Data Modeling", 
                    "Data Governance", "Master Data Management"
                ]
            },
            "DevOps": {
                "skills": [
                    "DevOps", "CI/CD Pipeline", "Containerization", "Kubernetes", 
                    "Infrastructure as Code", "Monitoring & Observability"
                ]
            }
        },
        "projects": {
            "Refonte application métier": {
                "tasks": {
                    "Analyse des besoins utilisateurs": {
                        "subtasks": [
                            "Entretiens avec les utilisateurs clés", 
                            "Revue des processus actuels",
                            "Identification des points de friction", 
                            "Priorisation des fonctionnalités"
                        ]
                    },
                    "Développement backend": {
                        "subtasks": [
                            "Conception API RESTful", 
                            "Implémentation modèle de données", 
                            "Développement logique d'authentification",
                            "Optimisation requêtes base de données", 
                            "Tests unitaires modules critiques", 
                            "Documentation technique API"
                        ]
                    },
                    "Développement interfaces utilisateur": {
                        "subtasks": [
                            "Maquettage des écrans", 
                            "Développement composants UI", 
                            "Implémentation logique client",
                            "Tests d'utilisabilité", 
                            "Optimisation responsive"
                        ]
                    },
                    "Migration des données": {
                        "subtasks": [
                            "Analyse données existantes", 
                            "Conception scripts migration", 
                            "Tests intégrité données",
                            "Validation migration", 
                            "Documentation processus"
                        ]
                    }
                }
            },
            "Développement plateforme analytique": {
                "tasks": {
                    "Conception architecture data": {
                        "subtasks": [
                            "Cartographie sources de données", 
                            "Conception data lake", 
                            "Définition flux ETL",
                            "Architecture temps réel"
                        ]
                    },
                    "Développement pipelines de données": {
                        "subtasks": [
                            "Implémentation connecteurs sources", 
                            "Développement jobs transformation", 
                            "Mise en place orchestration",
                            "Tests performance"
                        ]
                    }
                }
            },
            "Architecture microservices": {
                "tasks": {
                    "Conception architecture": {
                        "subtasks": [
                            "Décomposition domaines fonctionnels", 
                            "Définition interfaces API", 
                            "Conception modèle de données distribué",
                            "Stratégie de déploiement"
                        ]
                    }
                }
            }
        }
    },
    "Support_SI": {
        "name": "Support_SI",
        "skill_categories": {
            "Support utilisateur": {
                "skills": [
                    "IT Support", "Helpdesk", "User Training", 
                    "Troubleshooting", "Onboarding Support"
                ]
            },
            "Administration système": {
                "skills": [
                    "System Administration", "Windows Server", "Linux Administration", 
                    "Active Directory", "Group Policy Management"
                ]
            },
            "Infrastructure réseau": {
                "skills": [
                    "Network Administration", "LAN/WAN Configuration", "Network Security", 
                    "VPN Setup", "Firewall Management"
                ]
            },
            "Services cloud": {
                "skills": [
                    "Cloud Services", "SaaS Administration", "Microsoft 365", 
                    "Google Workspace", "Cloud Backup Solutions"
                ]
            },
            "Infrastructure": {
                "skills": [
                    "Infrastructure Management", "Server Deployment", "Datacenter Management", 
                    "Storage Solutions", "Virtualization"
                ]
            },
            "Cybersécurité": {
                "skills": [
                    "IT Security", "Security Monitoring", "Vulnerability Assessment", 
                    "Incident Response", "Security Compliance"
                ]
            }
        },
        "projects": {
            "Migration infrastructure cloud": {
                "tasks": {
                    "Audit infrastructure existante": {
                        "subtasks": [
                            "Inventaire des serveurs physiques", 
                            "Analyse des applications hébergées", 
                            "Cartographie réseau actuelle",
                            "Évaluation capacité stockage", 
                            "Mesure performances actuelles", 
                            "Identification points de vigilance"
                        ]
                    },
                    "Conception architecture cible": {
                        "subtasks": [
                            "Définition architecture cloud", 
                            "Sélection services managés", 
                            "Conception réseau virtuel",
                            "Stratégie de sécurité cloud", 
                            "Plan de haute disponibilité"
                        ]
                    }
                }
            },
            "Déploiement solution VDI": {
                "tasks": {
                    "Étude besoins utilisateurs": {
                        "subtasks": [
                            "Analyse profils utilisateurs", 
                            "Estimation capacités requises", 
                            "Définition expérience utilisateur",
                            "Catalogue applications"
                        ]
                    }
                }
            }
        }
    },
    "CONSULTING": {
        "name": "CONSULTING",
        "skill_categories": {
            "Management de projet": {
                "skills": [
                    "Project Management", "Agile Methodology", "Scrum Master", 
                    "PRINCE2", "PMP", "Project Portfolio Management"
                ]
            },
            "Analyse métier": {
                "skills": [
                    "Business Analysis", "Requirements Engineering", "Process Mapping", 
                    "Use Case Development", "Gap Analysis"
                ]
            },
            "Stratégie d'entreprise": {
                "skills": [
                    "Business Strategy", "Digital Transformation", "Change Management", 
                    "Organizational Design", "Process Optimization"
                ]
            },
            "Marketing": {
                "skills": [
                    "Marketing", "Market Research", "Digital Marketing", 
                    "Customer Experience", "Brand Strategy", "Go-to-Market Strategy"
                ]
            },
            "Analyse financière": {
                "skills": [
                    "Financial Analysis", "Cost-Benefit Analysis", "Budget Planning", 
                    "ROI Assessment", "Financial Modeling"
                ]
            },
            "Conseil en management": {
                "skills": [
                    "Management Consulting", "Executive Coaching", "Leadership Development", 
                    "Team Building", "Performance Management"
                ]
            },
            "Formation": {
                "skills": [
                    "Training Development", "Knowledge Transfer", "Learning Management", 
                    "Capability Development", "Skill Assessment"
                ]
            }
        },
        "projects": {
            "Accompagnement transformation digitale": {
                "tasks": {
                    "Diagnostic maturité digitale": {
                        "subtasks": [
                            "Analyse écosystème IT", 
                            "Évaluation compétences internes", 
                            "Benchmark concurrentiel",
                            "Identification opportunités digitales"
                        ]
                    },
                    "Plan de conduite du changement": {
                        "subtasks": [
                            "Analyse d'impact organisationnel", 
                            "Identification des parties prenantes", 
                            "Élaboration plan de communication",
                            "Conception modules de formation", 
                            "Définition indicateurs d'adoption", 
                            "Planning déploiement progressif"
                        ]
                    }
                }
            }
        }
    },
    "BID": {
        "name": "BID",
        "skill_categories": {
            "Gestion d'appels d'offres": {
                "skills": [
                    "Bidding", "Tender Management", "RFP Response", 
                    "Competitive Analysis", "Win Strategy Development"
                ]
            },
            "Rédaction de propositions": {
                "skills": [
                    "Proposal Writing", "Technical Writing", "Solution Design", 
                    "Value Proposition Development", "Pricing Strategy"
                ]
            },
            "Négociation": {
                "skills": [
                    "Contract Negotiation", "Terms & Conditions Review", "Legal Compliance", 
                    "Commercial Terms Negotiation", "Partnership Agreements"
                ]
            },
            "Estimation de projet": {
                "skills": [
                    "Project Estimation", "Cost Calculation", "Effort Estimation", 
                    "Risk Assessment", "Resource Planning"
                ]
            },
            "Veille stratégique": {
                "skills": [
                    "Market Intelligence", "Competitor Analysis", "Opportunity Tracking", 
                    "Industry Trend Analysis", "Client Relationship Management"
                ]
            },
            "Marketing d'offres": {
                "skills": [
                    "Solution Marketing", "Presentation Design", "Executive Briefing", 
                    "Demo Preparation", "Client Workshop Facilitation"
                ]
            }
        },
        "projects": {
            "Réponse appel d'offres secteur public": {
                "tasks": {
                    "Analyse du cahier des charges": {
                        "subtasks": [
                            "Identification exigences techniques", 
                            "Analyse critères d'évaluation", 
                            "Vérification conformité administrative",
                            "Identification points discriminants"
                        ]
                    },
                    "Élaboration proposition technique": {
                        "subtasks": [
                            "Analyse exigences fonctionnelles", 
                            "Benchmark solutions techniques", 
                            "Conception architecture proposée",
                            "Rédaction spécifications", 
                            "Élaboration planning implémentation", 
                            "Identification risques et mitigation"
                        ]
                    }
                }
            }
        }
    }
}


class DepartmentFactory(factory.Factory):
    class Meta:
        model = dict  # Simuler les objets Odoo

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Iterator([dept["name"] for dept in COMPANY_DATA.values()])
    active = True

class SkillCategoryFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    department_id = factory.SubFactory(DepartmentFactory)
    name = factory.LazyAttribute(
        lambda o: random.choice(list(COMPANY_DATA[o.department_id['name']]["skill_categories"].keys()))
    )

class SkillFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    description = factory.Faker('sentence')
    category_id = factory.SubFactory(SkillCategoryFactory)
    level = FuzzyChoice(['beginner', 'intermediate', 'advanced'])
    last_used = FuzzyDate(date.today() - timedelta(days=365), date.today())
    active = True
    @factory.lazy_attribute
    def name(self):
        # Get all available skills for this category
        available_skills = COMPANY_DATA[self.category_id['department_id']['name']]["skill_categories"][self.category_id['name']]["skills"]
        
        # Track already created skills (in memory)
        if not hasattr(SkillFactory, 'used_skills'):
            SkillFactory.used_skills = set()
        
        # Filter to keep only unused skills
        unused_skills = [skill for skill in available_skills if skill not in SkillFactory.used_skills]
        
        # Raise exception if no skills are available
        if not unused_skills:
            raise ValueError(f"No more skills available for category {self.category_id['name']}")
        
        # Choose a random skill from available ones
        selected_skill = random.choice(unused_skills)
        
        # Mark this skill as used
        SkillFactory.used_skills.add(selected_skill)
        
        return selected_skill

class EmployeeFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    name = factory.LazyAttribute(lambda o: f"{o.first_name} {o.last_name}")
    email = factory.LazyAttribute(lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}@example.com")
    raw_phone = factory.Faker('phone_number')  # This creates a phone with various formats
    phone = factory.LazyAttribute(lambda o: ''.join(filter(str.isdigit, o.raw_phone)))
    role = FuzzyChoice(['employee', 'manager', 'admin'])
    department_id = factory.SubFactory(DepartmentFactory)
    is_manager = factory.LazyAttribute(lambda o: o.role == 'manager')
    gender = FuzzyChoice(['male', 'female'])
    country = FuzzyChoice(['Cameroun', 'Senegal', 'Nigeria', 'Togo', 'Côte d\'Ivoire', 'Maurice'])
   
    @factory.post_generation
    def skill_rating_ids(self, create, extracted, **kwargs):
        if not create:
            return
        
        # On ajoutera les compétences après avoir créé tous les objets



# Définir le dictionnaire en dehors de la classe
_used_projects = defaultdict(set)

class ProjectFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(
        lambda o: ProjectFactory._get_unique_project(o.department_id['name'])
    )
    description = factory.Faker('paragraph')
    department_id = factory.SelfAttribute('employee_id.department_id')
    start_date = FuzzyDate(date.today() - timedelta(days=180), date.today() - timedelta(days=30))
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=random.randint(60, 365)))
    status = FuzzyChoice(['to_do', 'in_progress', 'done'])
    progress = FuzzyInteger(0, 100)
    
    @classmethod
    def _get_unique_project(cls, department_name):
        global _used_projects
        
        # Récupère tous les projets disponibles pour ce département
        available_projects = list(COMPANY_DATA[department_name]["projects"].keys())
        # Filtre pour ne garder que ceux qui n'ont pas encore été utilisés
        unused_projects = [p for p in available_projects if p not in _used_projects[department_name]]
        
        # Si tous les projets ont été utilisés, réinitialiser
        if not unused_projects:
            _used_projects[department_name].clear()
            unused_projects = available_projects
        
        # Choisir un projet non utilisé et le marquer comme utilisé
        chosen_project = random.choice(unused_projects)
        _used_projects[department_name].add(chosen_project)
        
        return chosen_project

class ProjectDeliveryFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    project_id = factory.SubFactory(ProjectFactory)
    employee_id = factory.SelfAttribute('project_id.employee_id')  # Le manager du projet
    on_time = factory.Faker('boolean', chance_of_getting_true=70)
    comments = factory.Faker('paragraph')
    delivery_date = factory.LazyAttribute(lambda o: o.project_id['end_date'] + timedelta(days=random.randint(-10, 10)))




# Définir le dictionnaire pour suivre les tâches utilisées
_used_tasks = defaultdict(lambda: defaultdict(set))

class TaskFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(
        lambda o: TaskFactory._get_unique_task(
            o.project_id['department_id']['name'], 
            o.project_id['name']
        )
    )
    description = factory.Faker('paragraph')
    project_id = factory.SubFactory(ProjectFactory)
    manager_id = factory.SelfAttribute('project_id.employee_id')  # Le manager du projet
    # employee_id sera défini plus tard (l'employé assigné)
    start_date = factory.LazyAttribute(lambda o: o.project_id['start_date'] + timedelta(days=random.randint(5, 30)))
    expected_end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=random.randint(15, 60)))
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=random.randint(7, 90)) if random.choice([True, False]) else None
    )
    progress = FuzzyFloat(0.0, 100.0)
    priority = FuzzyChoice(['low', 'medium', 'high'])
    status = FuzzyChoice(['to_do', 'in_progress', 'done'])
    
    @classmethod
    def _get_unique_task(cls, department_name, project_name):
        global _used_tasks
        
        # Récupère toutes les tâches disponibles pour ce projet dans ce département
        available_tasks = list(COMPANY_DATA[department_name]["projects"][project_name]["tasks"].keys())
        
        # Filtre pour ne garder que celles qui n'ont pas encore été utilisées
        unused_tasks = [t for t in available_tasks if t not in _used_tasks[department_name][project_name]]

        # Si toutes les tâches ont été utilisées, réinitialiser
        if not unused_tasks:
            _used_tasks[department_name][project_name].clear()
            unused_tasks = available_tasks
        
        # Choisir une tâche non utilisée et la marquer comme utilisée
        chosen_task = random.choice(unused_tasks)
        _used_tasks[department_name][project_name].add(chosen_task)
        
        return chosen_task



# Définir le dictionnaire pour suivre les sous-tâches utilisées
_used_subtasks = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

class SubtaskFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    task_id = factory.SubFactory(TaskFactory)
    name = factory.LazyAttribute(
        lambda o: SubtaskFactory._get_unique_subtask(
            o.task_id['project_id']['department_id']['name'],
            o.task_id['project_id']['name'],
            o.task_id['name']
        )
    )
    description = factory.Faker('paragraph')
    # employee_id sera le même que celui de la tâche parente
    start_date = factory.LazyAttribute(lambda o: o.task_id['start_date'] + timedelta(days=random.randint(1, 10)))
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=random.randint(3, 20)) if random.choice([True, False]) else None
    )
    status = FuzzyChoice(['in_progress', 'completed'])
    
    @classmethod
    def _get_unique_subtask(cls, department_name, project_name, task_name):
        global _used_subtasks
        
        # Récupère toutes les sous-tâches disponibles pour cette tâche
        available_subtasks = COMPANY_DATA[department_name]["projects"][project_name]["tasks"][task_name]["subtasks"]
        
        # Filtre pour ne garder que celles qui n'ont pas encore été utilisées
        unused_subtasks = [st for st in available_subtasks 
                          if st not in _used_subtasks[department_name][project_name][task_name]]
        
        # Si toutes les sous-tâches ont été utilisées, réinitialiser
        if not unused_subtasks:
            _used_subtasks[department_name][project_name][task_name].clear()
            unused_subtasks = available_subtasks
        
        # Choisir une sous-tâche non utilisée et la marquer comme utilisée
        chosen_subtask = random.choice(unused_subtasks)
        _used_subtasks[department_name][project_name][task_name].add(chosen_subtask)
        
        return chosen_subtask

class EmployeeRatingFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    # employee_id sera assigné plus tard
    # project_id sera assigné plus tard
    rating = FuzzyInteger(0, 10)
    on_time = factory.Faker('boolean', chance_of_getting_true=75)
    comments = factory.Faker('paragraph')
    evaluation_date = FuzzyDate(date.today() - timedelta(days=90), date.today())
    state = FuzzyChoice(['draft', 'submitted'])
    # manager_id = factory.Sequence(lambda n: n + 1)  # Simplification pour res.users

class SkillRatingFactory(factory.Factory):
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: n + 1)
    employee_id = factory.SubFactory(EmployeeFactory)
    skill_id = factory.SubFactory(SkillFactory)
    rating = FuzzyInteger(1, 5)
    comments = factory.Faker('paragraph')

# Fonction principale pour générer un jeu de données complet
def generate_qctracker_data(num_departments=None, num_managers=None, num_regular_employees=None, num_projects=None):
    """
    Génère un jeu complet de données pour QCTracker en respectant toutes les relations
    """
    # 1. Création des catégories de compétences et des compétences
    skill_categories = [SkillCategoryFactory() for _ in range(6)]
    skills = []
    for category in skill_categories:
        # 2-4 compétences par catégorie
        category_skills = [SkillFactory(category_id=category) for _ in range(random.randint(2, 4))]
        skills.extend(category_skills)
    
    # 2. Création des départements
    departments = [DepartmentFactory() for _ in range(num_departments)]

    # 1. Création des départements
   
    # num_regular_employees = 40  # 40 employés réguliers
# 2. Création d'un manager pour chaque département
    managers = []
    for dept in departments:
        manager = EmployeeFactory(
        department_id=dept,
        role='manager',
        is_manager=True
    )
    # Ajout d'un user_id factice pour éviter l'erreur dans les évaluations d'employés
        manager['user_id'] = manager['id']
        managers.append(manager)

# 3. Création des employés réguliers
    employees = []
    for _ in range(num_regular_employees):  # Utilisez num_regular_employees au lieu de num_employees
        dept = random.choice(departments)
        employee = EmployeeFactory(
        department_id=dept,
        role='employee',
        is_manager=False
    )
    # Ajout d'un user_id factice 
        employee['user_id'] = employee['id']
        employees.append(employee)

# 4. Ajout des managers à la liste complète des employés
    all_employees = employees + managers
    
    # 5. Création des projets (assignés à des managers)
    projects = []
    for _ in range(num_projects):
        manager = random.choice(managers)
        project = ProjectFactory(
            department_id=manager['department_id'],
            employee_id=manager  # Le manager du projet
        )
        projects.append(project)
    
    # 6. Création des livraisons de projets
    project_deliveries = []
    for project in projects:
        if project['status'] == 'done' or random.random() < 0.3:  # Seuls certains projets ont des livraisons
            delivery = ProjectDeliveryFactory(
                project_id=project,
                employee_id=project['employee_id']  # Le manager du projet
            )
            project_deliveries.append(delivery)
    
    # 7. Création des tâches et sous-tâches
    tasks = []
    subtasks = []
    
    for project in projects:
        # 2-6 tâches par projet
        num_tasks = random.randint(2, 6)
        for _ in range(num_tasks):
            # Attribution d'un employé à la tâche (du même département que le projet)
            dept_employees = [e for e in all_employees if e['department_id']['id'] == project['department_id']['id']]
            if not dept_employees:
                assigned_employee = random.choice(all_employees)
            else:
                assigned_employee = random.choice(dept_employees)
            
            task = TaskFactory(
                project_id=project,
                manager_id=project['employee_id'],
                employee_id=assigned_employee
            )
            tasks.append(task)
            
            # 1-4 sous-tâches par tâche
            num_subtasks = random.randint(1, 4)
            for _ in range(num_subtasks):
                subtask = SubtaskFactory(
                    task_id=task,
                    employee_id=task['employee_id']
                )
                subtasks.append(subtask)
    
    # 8. Création des évaluations d'employés
    employee_ratings = []
    for task in tasks:
    # On évalue directement la tâche au lieu d'évaluer l'employé par projet
        if random.random() < 0.7:  # 70% de chance d'évaluer une tâche
        # Récupérer le manager du projet associé à la tâche
            project = task['project_id']
            project_manager = project['employee_id']
        
            rating = EmployeeRatingFactory(
            employee_id=task['employee_id'],
            task_id=task,  # Référencer la tâche à la place du projet
            manager_id=project_manager
            )
            employee_ratings.append(rating)
    # 9. Création des évaluations de compétences
    skill_ratings = []
    for employee in all_employees:
    # Chaque employé a 2 à 5 compétences évaluées
       num_skills = random.randint(2, 5)
       employee_skills = random.sample(skills, min(num_skills, len(skills)))

    for skill in employee_skills:
        skill_rating = SkillRatingFactory(
            employee_id=employee,
            skill_id=skill,
            rating=random.choice(['1', '2', '3', '4'])  # 👈 Valeur string compatible
        )
        skill_ratings.append(skill_rating)

    
    # 10. Mise à jour des relations inversées
    for department in departments:
        department['employee_ids'] = [e for e in all_employees if e['department_id']['id'] == department['id']]
        department['project_ids'] = [p for p in projects if p['department_id']['id'] == department['id']]
    
    for employee in all_employees:
        employee['task_ids'] = [t for t in tasks if t['employee_id']['id'] == employee['id']]
        employee['rating_employee_ids'] = [r for r in employee_ratings if r['employee_id']['id'] == employee['id']]
        employee['skill_rating_ids'] = [s for s in skill_ratings if s['employee_id']['id'] == employee['id']]
        employee['project_ids'] = [p for p in projects if p['employee_id']['id'] == employee['id']]
        employee['project_delivery_ids'] = [d for d in project_deliveries if d['employee_id']['id'] == employee['id']]
    
    for project in projects:
        project['task_ids'] = [t for t in tasks if t['project_id']['id'] == project['id']]
        project['project_delivery_ids'] = [d for d in project_deliveries if d['project_id']['id'] == project['id']]
    
    for task in tasks:
        task['subtask_ids'] = [s for s in subtasks if s['task_id']['id'] == task['id']]
    
    # Regroupement des données
    return {
        'departments': departments,
        'skill_categories': skill_categories,
        'skills': skills,
        'employees': all_employees,
        'projects': projects,
        'project_deliveries': project_deliveries,
        'tasks': tasks,
        'subtasks': subtasks,
        'employee_ratings': employee_ratings,
        'skill_ratings': skill_ratings
    }


# Pour utiliser ce script directement (pas via Odoo)
if __name__ == "__main__":
    data = generate_qctracker_data()
    print(f"Générées: {len(data['departments'])} départements, {len(data['employees'])} employés")
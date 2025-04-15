import factory
import random
from datetime import date, timedelta
from factory.fuzzy import FuzzyDate, FuzzyFloat, FuzzyChoice, FuzzyInteger

# Définition des modèles Factory pour toutes les entités

class DepartmentFactory(factory.Factory):
    class Meta:
        model = dict  # Simuler les objets Odoo

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('department')
    active = True

class SkillCategoryFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('job')

class SkillFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('job')
    description = factory.Faker('sentence')
    category_id = factory.SubFactory(SkillCategoryFactory)
    level = FuzzyChoice(['beginner', 'intermediate', 'advanced'])
    last_used = FuzzyDate(date.today() - timedelta(days=365), date.today())
    active = True

class EmployeeFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    name = factory.LazyAttribute(lambda o: f"{o.first_name} {o.last_name}")
    email = factory.LazyAttribute(lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}@example.com")
    phone = factory.Faker('phone_number')
    role = FuzzyChoice(['employee', 'manager', 'admin'])
    department_id = factory.SubFactory(DepartmentFactory)
    is_manager = factory.LazyAttribute(lambda o: o.role == 'manager')
    gender = FuzzyChoice(['male', 'female'])
    country = FuzzyChoice(['Cameroun', 'Senegal', 'Nigeria', 'Togo', 'USA', 'Côte d\'Ivoire', 'Maurice'])
   

    @factory.post_generation
    def skill_rating_ids(self, create, extracted, **kwargs):
        if not create:
            return
        
        # On ajoutera les compétences après avoir créé tous les objets

class ProjectFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('catch_phrase')
    description = factory.Faker('paragraph')
    department_id = factory.SelfAttribute('employee_id.department_id')
    start_date = FuzzyDate(date.today() - timedelta(days=180), date.today() - timedelta(days=30))
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=random.randint(60, 365)))
    # employee_id référence au Manager (défini après les employés)
    status = FuzzyChoice(['to_do', 'in_progress', 'done'])
    progress = FuzzyInteger(0, 100)

class ProjectDeliveryFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    project_id = factory.SubFactory(ProjectFactory)
    employee_id = factory.SelfAttribute('project_id.employee_id')  # Le manager du projet
    on_time = factory.Faker('boolean', chance_of_getting_true=70)
    comments = factory.Faker('paragraph')
    delivery_date = factory.LazyAttribute(lambda o: o.project_id['end_date'] + timedelta(days=random.randint(-10, 10)))

class TaskFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('sentence', nb_words=6)
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

class SubtaskFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    task_id = factory.SubFactory(TaskFactory)
    name = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')
    # employee_id sera le même que celui de la tâche parente
    start_date = factory.LazyAttribute(lambda o: o.task_id['start_date'] + timedelta(days=random.randint(1, 10)))
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=random.randint(3, 20)) if random.choice([True, False]) else None
    )
    status = FuzzyChoice(['in_progress', 'completed'])

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
    manager_id = factory.Sequence(lambda n: n + 1)  # Simplification pour res.users

class SkillRatingFactory(factory.Factory):
    class Meta:
        model = dict
    
    id = factory.Sequence(lambda n: n + 1)
    employee_id = factory.SubFactory(EmployeeFactory)
    skill_id = factory.SubFactory(SkillFactory)
    rating = FuzzyInteger(1, 5)
    comments = factory.Faker('paragraph')

# Fonction principale pour générer un jeu de données complet
def generate_qctracker_data(num_departments=5, num_managers=7, num_employees=37, num_projects=8):
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
    
    # 3. Création des managers
    managers = []
    for _ in range(num_managers):
        dept = random.choice(departments)
        manager = EmployeeFactory(
            department_id=dept,
            role='manager',
            is_manager=True
        )
        managers.append(manager)
    
    # 4. Création des employés
    employees = []
    for _ in range(num_employees):
        dept = random.choice(departments)
        employee = EmployeeFactory(
            department_id=dept,
            role='employee',
            is_manager=False
        )
        employees.append(employee)
    
    # Ajout des managers à la liste complète des employés
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
    for project in projects:
        project_tasks = [t for t in tasks if t['project_id']['id'] == project['id']]
        rated_employees = set()
        
        for task in project_tasks:
            employee = task['employee_id']
            if employee['id'] not in rated_employees and random.random() < 0.7:  # 70% de chance d'être évalué
                rating = EmployeeRatingFactory(
                    employee_id=employee,
                    project_id=project,
                    manager_id=project['employee_id']['user_id']
                )
                employee_ratings.append(rating)
                rated_employees.add(employee['id'])
    
    # 9. Création des évaluations de compétences
    skill_ratings = []
    for employee in all_employees:
        # Chaque employé a 2-5 compétences évaluées
        num_skills = random.randint(2, 5)
        employee_skills = random.sample(skills, min(num_skills, len(skills)))
        
        for skill in employee_skills:
            skill_rating = SkillRatingFactory(
                employee_id=employee,
                skill_id=skill
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

# Exemple d'utilisation
if __name__ == "__main__":
    data = generate_qctracker_data()
    
   
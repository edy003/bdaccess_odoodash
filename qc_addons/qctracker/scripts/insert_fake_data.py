# import_fake_data.py
from .fake_data import generate_qctracker_data
import random
def run(env, num_departments=4, num_managers=4, num_regular_employees=40, num_projects=8):
    """
    Importe des données fictives dans la base de données Odoo
    
    Args:
        env: L'environnement Odoo
        num_departments: Nombre de départements à créer
        num_managers: Nombre de managers à créer 
        num_employees: Nombre d'employés à créer
        num_projects: Nombre de projets à créer
    
    Returns:
        dict: Un résumé des objets créés
    """
    data = generate_qctracker_data(
        num_departments=num_departments,
        num_managers=num_managers,
        num_regular_employees=num_regular_employees,
        num_projects=num_projects
    )

    # Récupération des modèles
    Department = env['qctracker.department']
    Employee = env['qctracker.employee']
    Project = env['qctracker.project']
    Task = env['qctracker.task']
    Subtask = env['qctracker.subtask']
    Rating = env['qctracker.employeerating']
    SkillRating = env['qctracker.skillrating']
    Skill = env['qctracker.skill']
    SkillCategory = env['qctracker.skill.category']
    Delivery = env['qctracker.projectdelivery']

    # 1. Catégories de compétences
    print("Import des catégories de compétences...")
    cat_map = {}
    for cat in data['skill_categories']:
        rec = SkillCategory.create({
            'name': cat['name']
        })
        cat_map[cat['id']] = rec.id
    
    # 2. Compétences
    print("Import des compétences...")
    skill_map = {}
    for skill in data['skills']:
        rec = Skill.create({
            'name': skill['name'],
            'description': skill['description'],
            'category_id': cat_map[skill['category_id']['id']],
            'level': skill['level'],
            'last_used': skill['last_used'],
            'active': skill['active']
        })
        skill_map[skill['id']] = rec.id

    # 3. Départements
    print("Import des départements...")
    dept_map = {}
    for dept in data['departments']:
        rec = Department.create({
            'name': dept['name'],
            'active': dept['active']
        })
        dept_map[dept['id']] = rec.id
    
    # 4. Employés
    print("Import des employés...")
    ALLOWED_COUNTRIES = ['Cameroun', 'Senegal', 'Nigeria', 'Togo', 'Côte d\'Ivoire', 'Maurice']
    emp_map = {}
    for emp in data['employees']:
        # Recherche du pays par nom
        country_id = env['res.country'].search([('name', '=', emp['country'])], limit=1).id
        if not country_id:
            random_country = random.choice(ALLOWED_COUNTRIES)
            country_id = env['res.country'].search([('name', '=', random_country)], limit=1).id
            
            
        rec = Employee.create({
            'name': emp['name'],
            'first_name': emp.get('first_name', ''),
            'last_name': emp.get('last_name', ''),
            'email': emp['email'],
            'phone': emp['phone'],
            'role': emp['role'],
            'department_id': dept_map[emp['department_id']['id']],
            'gender': emp['gender'],
            'is_manager': emp['is_manager'],
            'country_id': country_id
        })
        emp_map[emp['id']] = rec.id

    # 5. Projets
    print("Import des projets...")
    proj_map = {}
    for proj in data['projects']:
        rec = Project.create({
            'name': proj['name'],
            'description': proj['description'],
            'start_date': proj['start_date'],
            'end_date': proj['end_date'],
            'department_id': dept_map[proj['department_id']['id']],
            'employee_id': emp_map[proj['employee_id']['id']],
            'status': proj['status'],
            'progress': proj['progress']
        })
        proj_map[proj['id']] = rec.id

    # 6. Tâches
    print("Import des tâches...")
    task_map = {}
    for task in data['tasks']:
        rec = Task.create({
            'name': task['name'],
            'description': task['description'],
            'project_id': proj_map[task['project_id']['id']],
            'employee_id': emp_map[task['employee_id']['id']],
            'manager_id': emp_map[task['manager_id']['id']],
            'start_date': task['start_date'],
            'expected_end_date': task['expected_end_date'],
            'end_date': task['end_date'],
            'progress': task['progress'],
            'priority': task['priority'],
            'status': task['status'],
        })
        task_map[task['id']] = rec.id

    # 7. Sous-tâches
    print("Import des sous-tâches...")
    for sub in data['subtasks']:
        Subtask.create({
            'task_id': task_map[sub['task_id']['id']],
            'name': sub['name'],
            'description': sub['description'],
            'employee_id': emp_map[sub['employee_id']['id']],
            'start_date': sub['start_date'],
            'end_date': sub['end_date'],
            'status': sub['status'],
        })

    # 8. Livraisons de projets
    print("Import des livraisons de projet...")
    for d in data['project_deliveries']:
        Delivery.create({
            'project_id': proj_map[d['project_id']['id']],
            'employee_id': emp_map[d['employee_id']['id']],
            'delivery_date': d['delivery_date'],
            'comments': d['comments'],
            'on_time': d['on_time']
        })

    # 9. Notation employés
    print("Import des évaluations d'employés...")
    for note in data['employee_ratings']:
        Rating.create({
            'employee_id': emp_map[note['employee_id']['id']],
            'task_id': task_map[note['task_id']['id']],
            'rating': note['rating'],
            'on_time': note['on_time'],
            'comments': note['comments'],
            'evaluation_date': note['evaluation_date'],
            'state': note['state'],
            'manager_id': emp_map[note['manager_id']['id']]
        })

    # 10. Évaluations des compétences
    print("Import des évaluations de compétences...")
    for sr in data['skill_ratings']:
        SkillRating.create({
            'employee_id': emp_map[sr['employee_id']['id']],
            'skill_id': skill_map[sr['skill_id']['id']],
            'rating': sr['rating'],
            'comments': sr['comments']
        })

    result = {
        'departments': len(dept_map),
        'employees': len(emp_map),
        'projects': len(proj_map),
        'tasks': len(task_map),
        'skills': len(skill_map),
        'skill_categories': len(cat_map)
    }
    
    print("✅ Données fictives importées avec succès:")
    for k, v in result.items():
        print(f"  - {k}: {v}")
        
    return result
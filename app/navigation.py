"""Sections and permission-filtered destinations shared by the profile and section menus."""

MENU_SECTIONS = (
    ('english', 'Inglês', 'quest', (
        ('Palavras', 'english_word_list', 'english_words.view_englishword', 'quest', '/english-words/'),
        ('Avaliações', 'evaluation_list', 'evaluations.view_evaluation', 'quest', '/evaluations/'),
    )),
    ('tasks', 'Tarefas', 'quest', (
        ('Tarefas', 'task_list', 'tasks.view_task', 'quest', '/tasks/'),
        ('Categorias', 'category_list', 'categories.view_category', 'tag', '/categories/'),
        ('Tarefas recorrentes', 'recurring_task_list', 'recurring_tasks.view_recurringtask', 'repeat', '/recurring-tasks/'),
    )),
    ('projects', 'Projetos', 'projects', (
        ('Projetos', 'project_list', 'projects.view_project', 'projects', '/projects/'),
        ('Tarefas de projeto', 'project_task_list', 'project_tasks.view_projecttask', 'quest', '/project-tasks/'),
        ('Possíveis tarefas', 'possible_task_list', 'possible_tasks.view_possibletask', 'spark', '/possible-tasks/'),
    )),
    ('workouts', 'Treinos', 'calendar', (
        ('Treino', 'workout_list', 'workouts.view_workout', 'calendar', '/workouts/'),
        ('Histórico', 'workout_history', 'workouts.view_workoutsession', 'undo', '/workouts/'),
        ('Treinar', 'workout_train', 'workouts.view_workoutsession', 'play', '/workouts/'),
    )),
    ('shopping', 'Compras', 'quest', (
        ('Desejo comprar', 'purchase_wish_list', 'shopping.view_purchasewish', 'heart', '/shopping/wishes/'),
        ('Itens da feira', 'shopping_list', 'shopping.view_shoppinglist', 'check', '/shopping/'),
        ('Fazer feira', 'shopping_start', ('shopping.view_shoppinglist', 'shopping.view_shoppingsession'), 'quest', '/shopping/'),
        ('Histórico', 'shopping_history', 'shopping.view_shoppingsession', 'undo', '/shopping/'),
    )),
)


AREA_SHORTCUTS = {'english_word_list': ('Palavras', 'book'),
 'evaluation_list': ('Avaliações', 'assessment'),
 'recurring_task_list': ('Recorrentes', 'repeat'),
 'project_task_list': ('Tarefas', 'checklist'),
 'possible_task_list': ('Ideias', 'bulb'),
 'workout_list': ('Treino', 'dumbbell'),
 'workout_train': ('Treinar', 'play'),
 'shopping_list': ('Lista da feira', 'basket'),
 'shopping_start': ('Fazer feira', 'cart'),
 'shopping_history': ('Histórico', 'history'),
 'workout_history': ('Histórico', 'history')}


def get_menu_sections(user):
    if not user.is_authenticated:
        return []
    sections = []
    for slug, label, icon, destinations in MENU_SECTIONS:
        options = []
        for title, route, permissions, option_icon, prefix in destinations:
            permissions = (permissions,) if isinstance(permissions, str) else permissions
            if user.has_perms(permissions):
                area_label, area_icon = AREA_SHORTCUTS.get(route, (title, option_icon))
                options.append({'label': title, 'route': route, 'icon': option_icon, 'prefix': prefix,
                                'area_label': area_label, 'area_icon': area_icon})
        if options:
            sections.append({
                'slug': slug, 'label': label, 'icon': icon, 'options': options,
                'prefixes': ' '.join(dict.fromkeys(option['prefix'] for option in options)),
            })
    return sections


def navigation(request):
    return {'menu_sections': get_menu_sections(request.user)}

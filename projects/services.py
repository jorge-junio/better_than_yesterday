from .models import Project


def get_default_project():
    return Project.objects.filter(is_default=True).order_by('id').first()

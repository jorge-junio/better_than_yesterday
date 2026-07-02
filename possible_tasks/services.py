from django.shortcuts import get_object_or_404

from .models import PossibleTask


def get_possible_task(pk):
    return get_object_or_404(PossibleTask.objects.select_related('project'), pk=pk)


def link_possible_task_to_generated_object(possible_task, generated_object):
    generated_object.origin_possible_task = possible_task
    generated_object.save()
    return generated_object

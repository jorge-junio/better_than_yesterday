from django.urls import path

from . import views


urlpatterns = [
    path('possible-tasks/list/', views.PossibleTaskListView.as_view(), name='possible_task_list'),
    path('possible-tasks/create/', views.PossibleTaskCreateView.as_view(), name='possible_task_create'),
    path('possible-tasks/<int:pk>/update/', views.PossibleTaskUpdateView.as_view(), name='possible_task_update'),
    path('possible-tasks/<int:pk>/delete/', views.PossibleTaskDeleteView.as_view(), name='possible_task_delete'),
]

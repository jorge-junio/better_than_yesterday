from django.urls import path

from . import views


urlpatterns = [
    path('project-tasks/list/', views.ProjectTaskListView.as_view(), name='project_task_list'),
    path('project-tasks/create/', views.ProjectTaskCreateView.as_view(), name='project_task_create'),
    path('project-tasks/<int:pk>/detail/', views.ProjectTaskDetailView.as_view(), name='project_task_detail'),
    path('project-tasks/<int:pk>/update/', views.ProjectTaskUpdateView.as_view(), name='project_task_update'),
    path('project-tasks/<int:pk>/delete/', views.ProjectTaskDeleteView.as_view(), name='project_task_delete'),
    path('project-tasks/<int:pk>/toggle-complete/', views.ProjectTaskToggleCompleteView.as_view(), name='project_task_toggle_complete'),
]

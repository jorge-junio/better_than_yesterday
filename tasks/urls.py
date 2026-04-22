from django.urls import path

from . import views


urlpatterns = [
    path('tasks/list/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/detail/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/complete/', views.TaskToggleCompleteView.as_view(), name='task_toggle_complete'),
    path('tasks/<int:pk>/postpone/', views.TaskPostponeView.as_view(), name='task_postpone'),
]

from django.urls import path

from . import views


urlpatterns = [
    path('recurring-tasks/list/', views.RecurringTaskListView.as_view(), name='recurring_task_list'),
    path('recurring-tasks/create/', views.RecurringTaskCreateView.as_view(), name='recurring_task_create'),
    path('recurring-tasks/<int:pk>/detail/', views.RecurringTaskDetailView.as_view(), name='recurring_task_detail'),
    path('recurring-tasks/<int:pk>/update/', views.RecurringTaskUpdateView.as_view(), name='recurring_task_update'),
    path('recurring-tasks/<int:pk>/delete/', views.RecurringTaskDeleteView.as_view(), name='recurring_task_delete'),
]

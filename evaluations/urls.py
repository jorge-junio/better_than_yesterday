from django.urls import path

from . import views


urlpatterns = [
    path('evaluations/list/', views.EvaluationListView.as_view(), name='evaluation_list'),
    path('evaluations/create/', views.EvaluationCreateView.as_view(), name='evaluation_create'),
    path('evaluations/<int:pk>/quiz/', views.EvaluationQuizView.as_view(), name='evaluation_quiz'),
    path('evaluations/<int:pk>/detail/', views.EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('evaluations/<int:pk>/update/', views.EvaluationUpdateView.as_view(), name='evaluation_update'),
    path('evaluations/<int:pk>/delete/', views.EvaluationDeleteView.as_view(), name='evaluation_delete'),
]

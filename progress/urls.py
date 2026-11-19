from django.urls import path

from . import views


urlpatterns = [
    path('evolution/', views.EvolutionView.as_view(), name='evolution'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]

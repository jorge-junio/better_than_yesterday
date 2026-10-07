from django.urls import path

from . import views

urlpatterns = [
    path('shopping/', views.ListView.as_view(), name='shopping_list'),
    path('shopping/lists/create/', views.ListFormView.as_view(), name='shopping_list_create'),
    path('shopping/lists/<int:pk>/', views.ListDetailView.as_view(), name='shopping_list_detail'),
    path('shopping/lists/<int:pk>/edit/', views.ListFormView.as_view(), name='shopping_list_update'),
    path('shopping/lists/<int:list_id>/items/add/', views.ItemFormView.as_view(), name='shopping_item_create'),
    path('shopping/lists/<int:list_id>/items/<int:item_id>/edit/', views.ItemFormView.as_view(), name='shopping_item_update'),
    path('shopping/start/', views.StartView.as_view(), name='shopping_start'),
    path('shopping/history/', views.HistoryView.as_view(), name='shopping_history'),
    path('shopping/sessions/<int:pk>/', views.SessionView.as_view(), name='shopping_session'),
    path('shopping/sessions/<int:pk>/finish/', views.FinishView.as_view(), name='shopping_finish'),
    path('shopping/sessions/<int:pk>/cancel/', views.CancelView.as_view(), name='shopping_cancel'),
]

from django.urls import path

from . import views


urlpatterns = [
    path('english-words/list/', views.EnglishWordListView.as_view(), name='english_word_list'),
    path('english-words/create/', views.EnglishWordCreateView.as_view(), name='english_word_create'),
    path('english-words/<int:pk>/detail/', views.EnglishWordDetailView.as_view(), name='english_word_detail'),
    path('english-words/<int:pk>/update/', views.EnglishWordUpdateView.as_view(), name='english_word_update'),
    path('english-words/<int:pk>/delete/', views.EnglishWordDeleteView.as_view(), name='english_word_delete'),
]


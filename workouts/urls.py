from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workouts/create/', views.WorkoutFormView.as_view(), name='workout_create'),
    path('workouts/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('workouts/<int:pk>/edit/', views.WorkoutFormView.as_view(), name='workout_update'),
    path('workouts/<int:pk>/archive/', views.WorkoutArchiveView.as_view(), name='workout_archive'),
    path('workouts/<int:workout_id>/days/<int:source_weekday>/copy/', views.WorkoutDayCopyView.as_view(), name='workout_day_copy'),
    path('workouts/<int:workout_id>/exercises/add/', views.WorkoutExerciseFormView.as_view(), name='workout_exercise_create'),
    path('workouts/<int:workout_id>/exercises/<int:entry_id>/edit/', views.WorkoutExerciseFormView.as_view(), name='workout_exercise_update'),
    path('workouts/exercises/<int:entry_id>/remove/', views.WorkoutExerciseRemoveView.as_view(), name='workout_exercise_remove'),
    path('workouts/train/', views.TrainView.as_view(), name='workout_train'),
    path('workouts/history/', views.HistoryView.as_view(), name='workout_history'),
    path('workouts/sessions/<int:pk>/', views.SessionView.as_view(), name='workout_session'),
    path('workouts/sessions/<int:pk>/finish/', views.SessionFinishView.as_view(), name='workout_session_finish'),
    path('workouts/sets/<int:set_id>/record/', views.SessionSetView.as_view(), name='workout_set_record'),
    path('workouts/session-exercises/<int:exercise_id>/skip/', views.SessionSkipView.as_view(), name='workout_session_skip'),
]

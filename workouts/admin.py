from django.contrib import admin
from .models import Exercise, Workout, WorkoutExercise, WorkoutSession, SessionExercise, SessionSet


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    search_fields = ['name', 'owner__username']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'start_date', 'end_date', 'rest_seconds', 'is_active', 'is_archived']
    list_filter = ['is_active', 'is_archived']
    search_fields = ['name']


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'workout', 'weekday', 'sets_count', 'repetitions']
    list_filter = ['weekday']


class HistoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(HistoryAdmin):
    list_display = ['workout_name', 'owner', 'date', 'status']
    list_filter = ['status', 'date']


admin.site.register(SessionExercise, HistoryAdmin)
admin.site.register(SessionSet, HistoryAdmin)

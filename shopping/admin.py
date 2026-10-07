from django.contrib import admin

from . import models


class ShoppingItemInline(admin.TabularInline):
    model = models.ShoppingItem
    extra = 0


@admin.register(models.ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    inlines = [ShoppingItemInline]


class ShoppingSessionItemInline(admin.TabularInline):
    model = models.ShoppingSessionItem
    fields = ['name', 'quantity']
    readonly_fields = fields
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.ShoppingSession)
class ShoppingSessionAdmin(admin.ModelAdmin):
    list_display = ['list_name', 'owner', 'started_at', 'status', 'total']
    list_filter = ['status']
    readonly_fields = ['owner', 'shopping_list', 'list_name', 'started_at', 'finished_at', 'status', 'total']
    inlines = [ShoppingSessionItemInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

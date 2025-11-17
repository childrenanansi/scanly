from django.contrib import admin
from .models import MainModel, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['parent']

@admin.register(MainModel)
class MainModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'friend_link', 'is_paid', 'is_requested']
    list_filter = ['is_paid', 'is_requested', 'categories']
    filter_horizontal = ['categories']
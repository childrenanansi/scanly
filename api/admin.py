from django.contrib import admin
from .models import MainModel, Category, FriendLink

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['parent']

class FriendLinkInline(admin.TabularInline):
    model = FriendLink
    extra = 1

@admin.register(MainModel)
class MainModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_paid', 'is_requested']
    list_filter = ['is_paid', 'is_requested', 'categories']
    filter_horizontal = ['categories']
    inlines = [
        FriendLinkInline
    ]



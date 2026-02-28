from django.contrib import admin
from .models import MainModel, Category, FriendLink, FAQ

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'alias', 'parent']
    list_filter = ['parent']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active', 'for_home_page', 'for_category_pages']
    list_filter = ['is_active', 'for_home_page', 'for_category_pages', 'categories']
    filter_horizontal = ['categories']
    list_editable = ['order', 'is_active']
    search_fields = ['question', 'answer']

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



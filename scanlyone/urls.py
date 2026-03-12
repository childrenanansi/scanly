"""
URL configuration for scanlyone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from api.views import home, category_page, search_page, static_page, trending_accounts, best_accounts, free_accounts, new_accounts
from api.views import blog_list, blog_detail, blog_category
from api.sitemaps import StaticViewSitemap, CategorySitemap, NewsSitemap, NewsCategorySitemap

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'news': NewsSitemap,
    'news-categories': NewsCategorySitemap,
}

schema_view = get_schema_view(
    openapi.Info(
        title="Твой API",
        default_version='v1',
        description="Описание твоего API",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home, name='home'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('category/<slug:category_alias>/', category_page, name='category_page'),
    path('category/', category_page, name='category_all'),
    path('search/', search_page, name='search_page'),
    path('trending/', trending_accounts, name='trending_accounts'),
    path('best/', best_accounts, name='best_accounts'),
    path('free/', free_accounts, name='free_accounts'),
    path('new/', new_accounts, name='new_accounts'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/category/<slug:slug>/', blog_category, name='blog_category'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('<slug:page_name>/', static_page, name='static_page'),
]

# Для обслуживания медиа-файлов в разработке
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
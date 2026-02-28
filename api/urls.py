from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *
from scanlyone.settings import DEBUG
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'mainmodels', MainModelViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'friend-links', FriendLinkViewSet, basename='friendlink')

urlpatterns = [
    path('', include(router.urls)),
    path('home/', home, name='home'),
    path('api/categories/', api_categories, name='api_categories'),
    path('api/profiles/', api_profiles, name='api_profiles'),
    path('set-language/', set_language, name='set_language'),
]


if DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
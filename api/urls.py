from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'mainmodels', MainModelViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'friend-links', FriendLinkViewSet, basename='friendlink')

urlpatterns = [
    path('', include(router.urls))
]
from django.urls import path
from .views import MainModelListCreateView, MainModelDetailView

urlpatterns = [
    path('main-models/', MainModelListCreateView.as_view(), name='main-model-list-create'),
    path('main-models/<int:pk>/', MainModelDetailView.as_view(), name='main-model-detail'),
]
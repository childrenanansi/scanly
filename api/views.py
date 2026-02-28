from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.http import JsonResponse
from .models import MainModel, Category, FriendLink
from .serializers import MainModelSerializer, CategorySerializer, FriendLinkSerializer
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MainModelViewSet(viewsets.ModelViewSet):
    queryset = MainModel.objects.all()
    serializer_class = MainModelSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories']

    def get_queryset(self):
        queryset = MainModel.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        return queryset.distinct()

class FriendLinkPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class FriendLinkViewSet(viewsets.ReadOnlyModelViewSet):  # только чтение (если не нужно создавать отдельно)

    queryset = FriendLink.objects.select_related('main_model')
    serializer_class = FriendLinkSerializer  # ← полный сериализатор
    pagination_class = FriendLinkPagination

    def get_queryset(self):
        queryset = FriendLink.objects.select_related('main_model')
        main_model_id = self.request.query_params.get('main_model')
        if main_model_id:
            queryset = queryset.filter(main_model_id=main_model_id)
        return queryset

# Django views for frontend
def home(request):

    categories = Category.objects.all()
    featured_profiles = MainModel.objects.filter(is_paid=True)[:6]
    recent_profiles = MainModel.objects.all().order_by('-id')[:50]
    
    context = {
        'categories': categories,
        'featured_profiles': featured_profiles,
        'recent_profiles': recent_profiles,
    }
    return render(request, 'index.html', context)

def api_categories(request):
    """
    API endpoint для получения категорий
    """
    categories = Category.objects.all()
    data = []
    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'count': MainModel.objects.filter(categories=category).count()
        })
    return JsonResponse(data, safe=False)

def api_profiles(request):
    """
    API endpoint для получения профилей
    """
    profiles = MainModel.objects.all()
    data = []
    for profile in profiles:
        data.append({
            'id': profile.id,
            'name': profile.name,
            'description': profile.description,
            'avatar': profile.avatar.url if profile.avatar else None,
            'top_photo': profile.top_photo.url if profile.top_photo else None,
            'link_ak': profile.link_ak,
            'is_paid': profile.is_paid,
            'categories': [cat.name for cat in profile.categories.all()]
        })
    return JsonResponse(data, safe=False)
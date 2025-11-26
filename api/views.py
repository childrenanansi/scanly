from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
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
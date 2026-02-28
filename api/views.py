from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.http import JsonResponse
from .models import MainModel, Category, FriendLink, FAQ
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

    featured_profiles = MainModel.objects.filter(is_paid=True)[:6]
    recent_profiles = MainModel.objects.all().order_by('-id')[:50]
    
    # Получаем FAQ для главной страницы
    faqs = FAQ.objects.filter(
        is_active=True,
        for_home_page=True
    ).order_by('order')
    
    # Если нет кастомных FAQ, используем дефолтные
    if not faqs.exists():
        faqs = get_default_faqs()
    
    context = {
        'featured_profiles': featured_profiles,
        'recent_profiles': recent_profiles,
        'faqs': faqs,
    }
    return render(request, 'index.html', context)

def category_page(request, category_alias=None):
    """
    Страница категории с карточками профилей
    """
    selected_category = None
    profiles = MainModel.objects.all()
    
    if category_alias:
        try:
            selected_category = Category.objects.get(alias=category_alias)
            profiles = profiles.filter(categories=selected_category)
        except Category.DoesNotExist:
            selected_category = None
    
    # Сортируем все категории по алфавиту
    all_categories = Category.objects.all().order_by('name')
    
    # Получаем FAQ для категории
    faqs = FAQ.objects.filter(
        is_active=True,
        for_category_pages=True
    )
    
    if selected_category:
        faqs = faqs.filter(categories=selected_category)
    
    faqs = faqs.order_by('order')
    
    # Если нет кастомных FAQ, используем дефолтные
    if not faqs.exists():
        faqs = get_default_faqs()
    
    # Пагинация или ограничение количества
    profiles = profiles.order_by('-id')[:50]
    
    context = {
        'selected_category': selected_category,
        'profiles': profiles,
        'all_categories': all_categories,
        'faqs': faqs,
    }
    return render(request, 'category.html', context)

def get_default_faqs():
    """
    Возвращает дефолтные FAQ
    """
    default_faqs = [
        {
            'question': 'Как работает SCANLY?',
            'answer': 'SCANLY использует искусственный интеллект для анализа и подбора моделей на основе ваших предпочтений. Наш алгоритм учитывает множество параметров для точного matching.'
        },
        {
            'question': 'Как выбрать подходящую категорию?',
            'answer': 'Используйте плитку категорий вверху страницы для быстрой навигации. Каждая категория содержит модели с соответствующими интересами и специализацией.'
        },
        {
            'question': 'Можно ли фильтровать модели по нескольким категориям?',
            'answer': 'Да, вы можете использовать теги на карточках моделей для поиска по пересечению интересов и находить модели с несколькими категориями.'
        }
    ]
    return default_faqs

def search_page(request):
    """
    Страница поиска с фильтрацией по описанию и категориям
    """
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    
    profiles = MainModel.objects.all()
    all_categories = Category.objects.all().order_by('name')
    
    # Поиск по описанию
    if query:
        profiles = profiles.filter(description__icontains=query)
    
    # Фильтр по категории
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            profiles = profiles.filter(categories=category)
        except Category.DoesNotExist:
            pass
    
    profiles = profiles.order_by('-id')[:50]
    
    # Получаем FAQ для страницы поиска
    faqs = FAQ.objects.filter(
        is_active=True,
        for_category_pages=True
    ).order_by('order')
    
    if not faqs.exists():
        faqs = get_default_faqs()
    
    context = {
        'query': query,
        'selected_category_id': category_id,
        'profiles': profiles,
        'all_categories': all_categories,
        'faqs': faqs,
    }
    return render(request, 'search.html', context)

def static_page(request, page_name):
    """
    Обработчик для статических страниц
    """
    page_config = {
        'about': {
            'title': 'О проекте',
            'description': 'Узнайте больше о платформе SCANLY',
            'template': 'pages/about.html'
        },
        'how-it-works': {
            'title': 'Как это работает',
            'description': 'Подробное описание работы платформы',
            'template': 'pages/how_it_works.html'
        },
        'pricing': {
            'title': 'Тарифы',
            'description': 'Выберите подходящий тарифный план',
            'template': 'pages/pricing.html'
        },
        'support': {
            'title': 'Поддержка',
            'description': 'Мы всегда готовы помочь',
            'template': 'pages/support.html'
        },
        'terms': {
            'title': 'Условия использования',
            'description': 'Правила использования платформы',
            'template': 'pages/terms.html'
        },
        'privacy': {
            'title': 'Политика конфиденциальности',
            'description': 'Как мы защищаем ваши данные',
            'template': 'pages/privacy.html'
        },
        'faq': {
            'title': 'FAQ',
            'description': 'Часто задаваемые вопросы',
            'template': 'pages/faq.html'
        },
        'contacts': {
            'title': 'Контакты',
            'description': 'Свяжитесь с нами',
            'template': 'pages/contacts.html'
        }
    }
    
    if page_name not in page_config:
        return render(request, '404.html')
    
    config = page_config[page_name]
    
    # Для FAQ страницы получаем вопросы
    faqs = []
    if page_name == 'faq':
        faqs = FAQ.objects.filter(is_active=True).order_by('order')
        if not faqs.exists():
            faqs = get_default_faqs()
    
    context = {
        'page_title': config['title'],
        'page_description': config['description'],
        'faqs': faqs,
    }
    
    return render(request, config['template'], context)

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
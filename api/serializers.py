from rest_framework import serializers
from .models import MainModel, Category, FriendLink, FAQ
from .fields import Base64ImageField
from collections import OrderedDict


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']
    
    def get_name(self, obj):
        return obj.get_localized_name


class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()
    
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'order', 'is_active', 'for_home_page', 'for_category_pages', 'categories']
    
    def get_question(self, obj):
        return obj.get_localized_question
    
    def get_answer(self, obj):
        return obj.get_localized_answer

class FriendLinkNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendLink
        fields = ['url']
        ref_name = 'FriendLinkNested'
        validators = []

# Для отдельного API эндпоинта (полный)
class FriendLinkSerializer(serializers.ModelSerializer):
    main_model_id = serializers.IntegerField(source='main_model.id', read_only=True)
    main_model_name = serializers.CharField(source='main_model.name', read_only=True)

    class Meta:
        model = FriendLink
        fields = ['id', 'url', 'main_model_id', 'main_model_name']
        ref_name = 'FriendLink'

class MainModelSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    top_photo = Base64ImageField(required=False, allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )
    friend_links = FriendLinkNestedSerializer(many=True, required=False)

    class Meta:
        model = MainModel
        fields = [
            'id', 'name', 'description', 'avatar', 'top_photo',
            'link_ak', 'is_paid', 'categories', 'is_requested', 'friend_links'
        ]

    def _save_friend_links(self, instance, friend_links_data):
        """Сохраняет только уникальные friend_links, пропуская дубли."""
        if not friend_links_data:
            return

        # 1. Убираем дубли внутри входного списка
        seen_urls = set()
        unique_input_links = []
        for link in friend_links_data:
            url = link.get('url')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_input_links.append(link)

        # 2. Получаем уже существующие URL для этого main_model
        existing_urls = set(
            FriendLink.objects.all().values_list('url', flat=True)
        )

        # 3. Сохраняем только новые (уникальные и не существующие)
        for link_data in unique_input_links:
            url = link_data['url']
            if url not in existing_urls:
                FriendLink.objects.create(main_model=instance, url=url)
                existing_urls.add(url)  # на случай повтора в том же запросе

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        friend_links_data = validated_data.pop('friend_links', [])

        instance = MainModel.objects.create(**validated_data)
        instance.categories.set(categories_data)
        self._save_friend_links(instance, friend_links_data)
        return instance

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', None)
        friend_links_data = validated_data.pop('friend_links', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories_data is not None:
            instance.categories.set(categories_data)

        if friend_links_data is not None:
            # 🔥 Если хочешь ЗАМЕНИТЬ все ссылки — сначала удали старые:
            # instance.friend_links.all().delete()
            # Но если хочешь ДОБАВЛЯТЬ без удаления — используем логику выше:
            self._save_friend_links(instance, friend_links_data)

        return instance
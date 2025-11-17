from rest_framework import serializers
from .models import MainModel, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class MainModelSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    categories_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = MainModel
        fields = [
            'id', 'name', 'description', 'avatar', 'top_photo',
            'friend_link', 'is_paid', 'categories', 'categories_ids', 'is_requested'
        ]
        extra_kwargs = {
            'friend_link': {'validators': []}
        }

    def validate_friend_link(self, value):
        """Кастомная валидация уникальности ссылки"""
        if self.instance:  # Если это обновление существующей записи
            if MainModel.objects.filter(friend_link=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Запись с такой ссылкой уже существует")
        else:  # Если это создание новой записи
            if MainModel.objects.filter(friend_link=value).exists():
                raise serializers.ValidationError("Запись с такой ссылкой уже существует")
        return value

    def create(self, validated_data):
        categories_ids = validated_data.pop('categories_ids', [])
        instance = MainModel.objects.create(**validated_data)

        if categories_ids:
            instance.categories.set(categories_ids)

        return instance

    def update(self, instance, validated_data):
        categories_ids = validated_data.pop('categories_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories_ids is not None:
            instance.categories.set(categories_ids)

        return instance
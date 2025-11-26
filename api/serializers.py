# api/serializers.py
from rest_framework import serializers
from .models import MainModel, Category
from .fields import Base64ImageField  # импортируем наше поле

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']

class MainModelSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    top_photo = Base64ImageField(required=False, allow_null=True)
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )

    class Meta:
        model = MainModel
        fields = [
            'id', 'name', 'description', 'avatar', 'top_photo',
            'link_ak', 'friend_link', 'is_paid', 'categories', 'is_requested'
        ]

    def validate_link_ak(self, value):
        queryset = MainModel.objects.filter(link_ak=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Запись с таким link_ak уже существует.")
        return value

    def validate_friend_link(self, value):
        queryset = MainModel.objects.filter(friend_link=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Запись с таким friend_link уже существует.")
        return value
# api/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Родительская категория"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class MainModel(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    avatar = models.FileField(upload_to='avatars/', verbose_name="Аватарка")
    top_photo = models.FileField(upload_to='top_photos/', verbose_name="Фото верхнее")
    friend_link = models.CharField(
        max_length=500,
        verbose_name="Ссылка на друзей",
        unique=True
    )
    is_paid = models.BooleanField(default=False, verbose_name="Платная/бесплатно")
    categories = models.ManyToManyField(Category, verbose_name="Категория")
    is_requested = models.BooleanField(default=False, verbose_name="Просилась или нет")

    class Meta:
        verbose_name = "Основная модель"
        verbose_name_plural = "Основные модели"

    def __str__(self):
        return self.name
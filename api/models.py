# api/models.py
from django.db import models
from pytils.translit import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    alias = models.SlugField(max_length=200, unique=True, verbose_name="Alias для URL",
        null=True,
        blank=True,)
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
    
    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = slugify(self.name)
        super().save(*args, **kwargs)

class FAQ(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    # Связи с категориями и страницами
    categories = models.ManyToManyField(Category, blank=True, verbose_name="Категории")
    for_home_page = models.BooleanField(default=False, verbose_name="Для главной страницы")
    for_category_pages = models.BooleanField(default=True, verbose_name="Для страниц категорий")

    class Meta:
        verbose_name = "Частый вопрос"
        verbose_name_plural = "Частые вопросы"
        ordering = ['order']

    def __str__(self):
        return self.question[:100]

class MainModel(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    avatar = models.FileField(upload_to='avatars/', verbose_name="Аватарка")
    top_photo = models.FileField(upload_to='top_photos/', verbose_name="Фото верхнее")
    link_ak = models.CharField(
        max_length=500,
        verbose_name="Ссылка на аккаунт",
        unique=True, null=True, blank=True
    )
    is_paid = models.BooleanField(default=False, verbose_name="Платная/бесплатно")
    categories = models.ManyToManyField(Category, verbose_name="Категория", null=True, blank=True)
    is_requested = models.BooleanField(default=False, verbose_name="Просилась или нет")

    class Meta:
        verbose_name = "Основная модель"
        verbose_name_plural = "Основные модели"

    def __str__(self):
        return self.name

class FriendLink(models.Model):
    main_model = models.ForeignKey(MainModel, related_name='friend_links', on_delete=models.CASCADE)
    url = models.URLField(max_length=500, verbose_name="Ссылка на друга")

    class Meta:
        verbose_name = "Ссылка на друга"
        verbose_name_plural = "Ссылки на друзей"
        unique_together = ('url',)

    def __str__(self):
        return self.url
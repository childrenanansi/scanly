# api/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from pytils.translit import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название (RU)",
        null=True,
        blank=True)
    name_ru = models.CharField(max_length=200, verbose_name="Название (RU)",
        null=True,
        blank=True)
    name_en = models.CharField(max_length=200, verbose_name="Name (EN)",
        null=True,
        blank=True)
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
        return self.get_localized_name
    
    @property
    def get_localized_name(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.name_en or self.name_ru or ''
        return self.name_ru or ''
    
    def save(self, *args, **kwargs):
        if not self.alias:
            # Use Russian name for alias by default
            self.alias = slugify(self.name_ru)
        super().save(*args, **kwargs)

class FAQ(models.Model):
    question_ru = models.TextField(verbose_name="Вопрос (RU)",
        null=True,
        blank=True)
    question_en = models.TextField(verbose_name="Question (EN)",
        null=True,
        blank=True)
    answer_ru = models.TextField(verbose_name="Ответ (RU)",
        null=True,
        blank=True)
    answer_en = models.TextField(verbose_name="Answer (EN)",
        null=True,
        blank=True)
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
        return self.get_localized_question[:100]
    
    @property
    def get_localized_question(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.question_en or self.question_ru or ''
        return self.question_ru or ''
    
    @property
    def get_localized_answer(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.answer_en or self.answer_ru or ''
        return self.answer_ru or ''

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
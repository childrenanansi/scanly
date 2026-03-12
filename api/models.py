from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from pytils.translit import slugify
from ckeditor.fields import RichTextField
import uuid

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

class NewsCategory(models.Model):
    name_ru = models.CharField(max_length=200, verbose_name="Название (RU)")
    name_en = models.CharField(max_length=200, verbose_name="Name (EN)")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    description_ru = RichTextField(blank=True, null=True, verbose_name="Описание (RU)")
    description_en = RichTextField(blank=True, null=True, verbose_name="Description (EN)")
    meta_title_ru = models.CharField(max_length=200, blank=True, null=True, verbose_name="Meta Title (RU)")
    meta_title_en = models.CharField(max_length=200, blank=True, null=True, verbose_name="Meta Title (EN)")
    meta_description_ru = models.TextField(blank=True, null=True, verbose_name="Meta Description (RU)")
    meta_description_en = models.TextField(blank=True, null=True, verbose_name="Meta Description (EN)")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")

    class Meta:
        verbose_name = "Категория новостей"
        verbose_name_plural = "Категории новостей"
        ordering = ['order', 'name_ru']

    def __str__(self):
        return self.get_localized_name

    @property
    def get_localized_name(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.name_en or self.name_ru
        return self.name_ru

    @property
    def get_localized_description(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.description_en or self.description_ru
        return self.description_ru

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_ru)
        super().save(*args, **kwargs)


class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'Архив'),
    ]

    title_ru = models.CharField(max_length=300, verbose_name="Заголовок (RU)")
    title_en = models.CharField(max_length=300, verbose_name="Title (EN)")
    slug = models.SlugField(max_length=300, unique=True, verbose_name="URL")
    
    # SEO поля
    meta_title_ru = models.CharField(max_length=200, blank=True, null=True, verbose_name="Meta Title (RU)")
    meta_title_en = models.CharField(max_length=200, blank=True, null=True, verbose_name="Meta Title (EN)")
    meta_description_ru = models.TextField(blank=True, null=True, verbose_name="Meta Description (RU)")
    meta_description_en = models.TextField(blank=True, null=True, verbose_name="Meta Description (EN)")
    meta_keywords_ru = models.CharField(max_length=200, blank=True, null=True, verbose_name="Meta Keywords (RU)")
    meta_keywords_en = models.CharField(max_length=200, blank=True, null=True, verbose_name="Meta Keywords (EN)")
    
    # Контент
    short_description_ru = RichTextField(verbose_name="Краткое описание (RU)")
    short_description_en = RichTextField(verbose_name="Short Description (EN)")
    content_ru = RichTextField(verbose_name="Содержание (RU)")
    content_en = RichTextField(verbose_name="Content (EN)")
    
    # Изображения
    preview_image = models.ImageField(upload_to='blog/previews/', verbose_name="Превью-изображение")
    main_image = models.ImageField(upload_to='blog/main/', blank=True, null=True, verbose_name="Основное изображение")
    
    # Автор и экспертиза (E-E-A-T)
    author_name = models.CharField(max_length=200, verbose_name="Имя автора")
    author_bio_ru = RichTextField(blank=True, null=True, verbose_name="Биография автора (RU)")
    author_bio_en = RichTextField(blank=True, null=True, verbose_name="Author Bio (EN)")
    author_avatar = models.ImageField(upload_to='blog/authors/', blank=True, null=True, verbose_name="Фото автора")
    
    # Экспертная информация
    expert_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Имя эксперта (проверил)")
    expert_title_ru = models.CharField(max_length=200, blank=True, null=True, verbose_name="Должность эксперта (RU)")
    expert_title_en = models.CharField(max_length=200, blank=True, null=True, verbose_name="Expert Title (EN)")
    expert_avatar = models.ImageField(upload_to='blog/experts/', blank=True, null=True, verbose_name="Фото эксперта")
    
    # Даты и статус
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    # Связи
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    tags = models.CharField(max_length=500, blank=True, null=True, verbose_name="Теги (через запятую)")
    
    # SEO и аналитика
    view_count = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    reading_time = models.PositiveIntegerField(default=5, verbose_name="Время чтения (минут)")
    
    # Настройки
    is_featured = models.BooleanField(default=False, verbose_name="Избранная новость")
    is_breaking = models.BooleanField(default=False, verbose_name="Срочная новость")
    allow_comments = models.BooleanField(default=True, verbose_name="Разрешить комментарии")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.get_localized_title

    @property
    def get_localized_title(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.title_en or self.title_ru
        return self.title_ru

    @property
    def get_localized_short_description(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.short_description_en or self.short_description_ru
        return self.short_description_ru

    @property
    def get_localized_content(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.content_en or self.content_ru
        return self.content_ru

    @property
    def get_localized_meta_title(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.meta_title_en or self.meta_title_ru or self.title_en or self.title_ru
        return self.meta_title_ru or self.title_ru

    @property
    def get_localized_meta_description(self):
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en':
            return self.meta_description_en or self.meta_description_ru or self.short_description_en or self.short_description_ru
        return self.meta_description_ru or self.short_description_ru

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def get_tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_ru)
        
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
            
        super().save(*args, **kwargs)
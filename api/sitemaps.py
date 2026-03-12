"""
Sitemap для автоматической генерации sitemap.xml
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category, News, NewsCategory


class StaticViewSitemap(Sitemap):
    """Статические страницы и основные разделы"""
    protocol = 'https'
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return [
            ('home', 1.0),
            ('blog_list', 0.9),
            ('trending_accounts', 0.9),
            ('best_accounts', 0.9),
            ('free_accounts', 0.9),
            ('new_accounts', 0.9),
            ('search_page', 0.7),
            ('about', 0.6),
            ('how-it-works', 0.6),
            ('pricing', 0.6),
            ('support', 0.6),
            ('terms', 0.5),
            ('privacy', 0.5),
            ('faq', 0.6),
            ('contacts', 0.6),
        ]

    def location(self, item):
        name, _ = item
        if name in ('about', 'how-it-works', 'pricing', 'support', 'terms', 'privacy', 'faq', 'contacts'):
            return reverse('static_page', kwargs={'page_name': name})
        return reverse(name)

    def priority(self, item):
        return item[1]


class CategorySitemap(Sitemap):
    """Страницы категорий из БД"""
    protocol = 'https'
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('category_page', kwargs={'category_alias': obj.alias})


class NewsSitemap(Sitemap):
    """Новости блога"""
    protocol = 'https'
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return News.objects.filter(status='published').order_by('-published_at')

    def location(self, obj):
        return reverse('blog_detail', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at or obj.published_at


class NewsCategorySitemap(Sitemap):
    """Категории новостей"""
    protocol = 'https'
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return NewsCategory.objects.filter(is_active=True).order_by('order')

    def location(self, obj):
        return reverse('blog_category', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at

from django.contrib import admin
from .models import MainModel, Category, FriendLink, FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['get_localized_question', 'order', 'is_active', 'for_home_page', 'for_category_pages']
    list_filter = ['is_active', 'for_home_page', 'for_category_pages', 'categories']
    filter_horizontal = ['categories']
    list_editable = ['order', 'is_active']
    search_fields = ['question_ru', 'question_en', 'answer_ru', 'answer_en']
    
    def get_localized_question(self, obj):
        return obj.get_localized_question
    get_localized_question.short_description = 'Вопрос'
    
    fieldsets = (
        ('Вопрос (RU)', {
            'fields': ('question_ru',)
        }),
        ('Вопрос (EN)', {
            'fields': ('question_en',)
        }),
        ('Ответ (RU)', {
            'fields': ('answer_ru',)
        }),
        ('Ответ (EN)', {
            'fields': ('answer_en',)
        }),
        ('Настройки', {
            'fields': ('order', 'is_active', 'for_home_page', 'for_category_pages', 'categories')
        }),
    )

class FriendLinkInline(admin.TabularInline):
    model = FriendLink
    extra = 1

@admin.register(MainModel)
class MainModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_paid', 'is_requested']
    list_filter = ['is_paid', 'is_requested', 'categories']
    filter_horizontal = ['categories']
    inlines = [
        FriendLinkInline
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['get_localized_name', 'alias', 'parent']
    list_filter = ['parent']
    fieldsets = (
        (None, {
            'fields': ('name', 'name_ru', 'name_en', 'alias', 'parent')
        }),
    )
    actions = ['make_published']

    def get_localized_name(self, obj):
        return obj.get_localized_name

    get_localized_name.short_description = 'Название'

    @admin.action(description='Импорт категорий')
    def make_published(self, request, queryset):
        default_categories = [
            {'name_ru': 'Фетиш', 'name_en': 'Fetish'},
            {'name_ru': 'Секстинг', 'name_en': 'Sexting'},
            {'name_ru': 'Ступни', 'name_en': 'Feet'},
            {'name_ru': 'Ню', 'name_en': 'Nude'},
            {'name_ru': 'PPV (Платный контент)', 'name_en': 'PPV'},
            {'name_ru': 'Милф', 'name_en': 'MILF'},
            {'name_ru': 'Секс', 'name_en': 'Sex'},
            {'name_ru': 'Кинк', 'name_en': 'Kink'},
            {'name_ru': 'Анал', 'name_en': 'Anal'},
            {'name_ru': 'Киска', 'name_en': 'Pussy'},
            {'name_ru': 'Латина', 'name_en': 'Latina'},
            {'name_ru': 'Миниатюрные', 'name_en': 'Petite'},
            {'name_ru': 'Косплей', 'name_en': 'Cosplay'},
            {'name_ru': 'Пышные формы', 'name_en': 'BBW'},
            {'name_ru': 'Порно', 'name_en': 'Porn'},
            {'name_ru': 'Любительское', 'name_en': 'Amateur'},
            {'name_ru': 'Блондинки', 'name_en': 'Blonde'},
            {'name_ru': 'JOI (Мастурбация по инструкции)', 'name_en': 'JOI'},
            {'name_ru': 'Студентки', 'name_en': 'Student'},
            {'name_ru': 'Мамы', 'name_en': 'Mom'},
            {'name_ru': 'Сквирт', 'name_en': 'Squirting'},
            {'name_ru': 'Бисексуалы', 'name_en': 'Bisexual'},
            {'name_ru': 'Транс', 'name_en': 'Trans'},
            {'name_ru': 'Девушки', 'name_en': 'Girls'},
            {'name_ru': 'Snapchat', 'name_en': 'Snapchat'},
            {'name_ru': 'Оценка достоинства', 'name_en': 'Dick Rating'},
            {'name_ru': 'Финдом', 'name_en': 'Findom'},
            {'name_ru': 'Азиатки', 'name_en': 'Asian'},
            {'name_ru': 'Готы', 'name_en': 'Goth'},
            {'name_ru': 'Фемдом', 'name_en': 'Femdom'},
            {'name_ru': 'Самые горячие', 'name_en': 'Hottest'},
            {'name_ru': 'Дилдо', 'name_en': 'Dildo'},
            {'name_ru': 'Безумные', 'name_en': 'Freaky'},
            {'name_ru': 'Британки', 'name_en': 'British'},
            {'name_ru': 'Рыжие', 'name_en': 'Redhead'},
            {'name_ru': 'Пухлые', 'name_en': 'Chubby'},
            {'name_ru': 'Сквирт', 'name_en': 'Squirt'},
            {'name_ru': 'Мамочки', 'name_en': 'Mommy'},
            {'name_ru': 'Геи', 'name_en': 'Gay'},
            {'name_ru': 'POV (От первого лица)', 'name_en': 'POV'},
            {'name_ru': 'Брюнетки', 'name_en': 'Brunette'},
            {'name_ru': 'Мужчины', 'name_en': 'Male'},
            {'name_ru': 'Жены-развратницы', 'name_en': 'Hotwife'},
            {'name_ru': 'Бондаж', 'name_en': 'Bondage'},
            {'name_ru': 'Негроидки', 'name_en': 'Ebony'},
            {'name_ru': 'SPH (Маленький член)', 'name_en': 'SPH'},
            {'name_ru': 'Большая попа', 'name_en': 'Big Ass'},
            {'name_ru': 'Reddit', 'name_en': 'Reddit'},
            {'name_ru': 'Йога', 'name_en': 'Yoga'},
            {'name_ru': 'Госпожи', 'name_en': 'Mistress'},
            {'name_ru': 'Немки', 'name_en': 'German'},
            {'name_ru': 'Грудастые', 'name_en': 'Busty'},
            {'name_ru': 'Канадки', 'name_en': 'Canadian'},
            {'name_ru': 'Минет', 'name_en': 'Blowjob'},
            {'name_ru': 'Лесбиянки', 'name_en': 'Lesbian'},
            {'name_ru': 'Пары', 'name_en': 'Couples'},
            {'name_ru': 'Твинки', 'name_en': 'Twink'},
            {'name_ru': 'TikTok', 'name_en': 'TikTok'},
            {'name_ru': 'Волосатые', 'name_en': 'Hairy'},
            {'name_ru': 'Большая грудь', 'name_en': 'Big Tits'},
            {'name_ru': 'Француженки', 'name_en': 'French'},
            {'name_ru': 'Ирландки', 'name_en': 'Irish'},
            {'name_ru': 'Тату', 'name_en': 'Tattoo'},
            {'name_ru': 'BBC (Большой черный член)', 'name_en': 'BBC'},
            {'name_ru': 'Хардкор', 'name_en': 'Hardcore'},
            {'name_ru': 'Большие сиськи', 'name_en': 'Big Boobs'},
            {'name_ru': 'Порнозвезды', 'name_en': 'Pornstar'},
            {'name_ru': 'Шлюхи', 'name_en': 'Whore'},
            {'name_ru': 'Индиянки', 'name_en': 'Indian'},
            {'name_ru': 'Сисси', 'name_en': 'Sissy'},
            {'name_ru': 'Австралийки', 'name_en': 'Australian'},
            {'name_ru': 'PAWG (Белая девушка с большой попой)', 'name_en': 'PAWG'},
            {'name_ru': 'Японки', 'name_en': 'Japanese'},
            {'name_ru': 'Трансгендеры', 'name_en': 'TS'},
            {'name_ru': 'Фембои', 'name_en': 'Femboy'},
            {'name_ru': 'Шотландки', 'name_en': 'Scottish'},
            {'name_ru': 'Учительницы', 'name_en': 'Teacher'},
            {'name_ru': 'Грузинки', 'name_en': 'Georgia'},
            {'name_ru': 'Кореянки', 'name_en': 'Korean'},
            {'name_ru': 'Майами', 'name_en': 'Miami'},
            {'name_ru': 'Домохозяйки', 'name_en': 'Housewife'},
            {'name_ru': 'Кремпи', 'name_en': 'Creampie'},
            {'name_ru': 'Русские', 'name_en': 'Russian'},
            {'name_ru': 'Качки', 'name_en': 'Muscle'},
            {'name_ru': 'Зрелые', 'name_en': 'Mature'},
            {'name_ru': 'Шведки', 'name_en': 'Swedish'},
            {'name_ru': 'Худые', 'name_en': 'Skinny'},
            {'name_ru': 'Беременные', 'name_en': 'Pregnant'},
            {'name_ru': 'Тайки', 'name_en': 'Thai'},
            {'name_ru': 'Колумбийки', 'name_en': 'Colombian'},
            {'name_ru': 'Трансгендеры', 'name_en': 'Transgender'},
            {'name_ru': 'Филиппинки', 'name_en': 'Filipina'},
            {'name_ru': 'Латвия', 'name_en': 'Latvia'},
            {'name_ru': 'Свингеры', 'name_en': 'Swinger'},
            {'name_ru': 'Fansly', 'name_en': 'Fansly'},
            {'name_ru': 'Pornhub', 'name_en': 'Pornhub'},
            {'name_ru': 'Самые грязные', 'name_en': 'Dirtiest'},
            {'name_ru': 'Тройничок', 'name_en': 'Threesome'},
            {'name_ru': 'Межрасовое', 'name_en': 'Interracial'},
        ]

        for cat_data in default_categories:
            category, created = Category.objects.get_or_create(
                name_ru=cat_data['name_ru'],
                defaults={
                    'name': cat_data['name_ru'],
                    'name_en': cat_data['name_en'],
                    'alias': cat_data['name_en'].lower().replace(' & ', '_').replace(' ', '_')
                }
            )
        self.message_user(request, f'✅ Опубликовано: ')

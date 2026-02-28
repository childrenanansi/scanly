from django.core.management.base import BaseCommand
from api.models import Category, FAQ


class Command(BaseCommand):
    help = 'Migrate existing data to multilingual fields'

    def handle(self, *args, **options):
        # Migrate Categories
        categories = Category.objects.all()
        for category in categories:
            if hasattr(category, 'name_ru') and not category.name_en:
                # Copy Russian name to English field if English is empty
                category.name_en = category.name_ru
                category.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Migrated category: {category.name_ru}')
                )
        
        # Migrate FAQs
        faqs = FAQ.objects.all()
        for faq in faqs:
            if hasattr(faq, 'question_ru') and not faq.question_en:
                # Copy Russian content to English fields if English is empty
                faq.question_en = faq.question_ru
                faq.answer_en = faq.answer_ru
                faq.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Migrated FAQ: {faq.question_ru[:50]}...')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Migration completed successfully!')
        )

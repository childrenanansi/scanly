# Generated migration to fix data loss during multilingual migration

from django.db import migrations, models


def copy_category_data(apps, schema_editor):
    """Copy data from old name field to new name_ru field"""
    Category = apps.get_model('api', 'Category')
    for category in Category.objects.all():
        if hasattr(category, 'name') and category.name:
            category.name_ru = category.name
            category.name_en = category.name  # Copy to both for now
            category.save()


def copy_faq_data(apps, schema_editor):
    """Copy data from old fields to new multilingual fields"""
    FAQ = apps.get_model('api', 'FAQ')
    for faq in FAQ.objects.all():
        if hasattr(faq, 'question') and faq.question:
            faq.question_ru = faq.question
            faq.question_en = faq.question  # Copy to both for now
        if hasattr(faq, 'answer') and faq.answer:
            faq.answer_ru = faq.answer
            faq.answer_en = faq.answer  # Copy to both for now
        faq.save()


def reverse_copy_data(apps, schema_editor):
    """Reverse function - no action needed"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_category_name_remove_faq_answer_and_more'),
    ]

    operations = [
        # Add temporary data migration
        migrations.RunPython(copy_category_data, reverse_copy_data),
        migrations.RunPython(copy_faq_data, reverse_copy_data),
    ]

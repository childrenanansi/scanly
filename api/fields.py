import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Проверяем, что строка — это base64
        if isinstance(data, str) and data.startswith('data:image'):
            # Обрабатываем формат: data:image/png;base64,iVBOR...
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]  # например, 'png', 'jpeg'

            # Генерируем уникальное имя
            filename = f"{uuid.uuid4().hex}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=filename)

        return super().to_internal_value(data)
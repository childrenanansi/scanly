from rest_framework import generics, status
from rest_framework.response import Response
from .models import MainModel
from .serializers import MainModelSerializer


class MainModelListCreateView(generics.ListCreateAPIView):
    queryset = MainModel.objects.all()
    serializer_class = MainModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Дополнительная проверка уникальности friend_link
        friend_link = serializer.validated_data.get('friend_link')
        if MainModel.objects.filter(friend_link=friend_link).exists():
            return Response(
                {"friend_link": ["Запись с такой ссылкой уже существует"]},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MainModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MainModel.objects.all()
    serializer_class = MainModelSerializer
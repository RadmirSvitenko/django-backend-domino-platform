from rest_framework.response import Response
from rest_framework import viewsets, filters
from .models import Ad, AdLike
from .filters import AdFilter
from django_filters import rest_framework as dj_filters
from .serializers import AdSerializer
from .pagination import CustomPagination
from rest_framework.decorators import action

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = CustomPagination
    filter_backends = (dj_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = AdFilter
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        ad = self.get_object()
        ad.views += 1
        ad.save()
        serializer = self.get_serializer(ad)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def toggle_like(self, request, pk=None):
        ad = self.get_object()
        ip_address = request.META.get('REMOTE_ADDR')  # Получаем IP-адрес клиента

        # Проверяем, есть ли уже лайк от этого IP для данного объявления
        ad_like, created = AdLike.objects.get_or_create(ad=ad, ip_address=ip_address)

        if not created:  # Если лайк уже был поставлен, удаляем его
            ad.likes -= 1
            ad_like.delete()
            return Response({'message': 'Like removed', 'likes': ad.likes})
        else:  # Если лайка еще не было, увеличиваем количество лайков
            ad.likes += 1
            return Response({'message': 'Like added', 'likes': ad.likes})

        ad.save()
        return Response({'likes': ad.likes})
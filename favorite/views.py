from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from favorite.models import Favorite
from favorite.serializers import FavoriteSerializer


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем избранное для текущего пользователя
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

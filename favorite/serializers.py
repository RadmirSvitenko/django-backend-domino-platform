from ad.serializers import AdSerializer
from .models import Favorite
from rest_framework import serializers
from ad.models import Ad
class FavoriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=True)  # ID пользователя для POST и PUT
    ad_id = serializers.IntegerField(write_only=True, required=True)  # ID объявления для POST и PUT
    ads = AdSerializer(many=True, read_only=True)  # Список объектов Ad при GET

    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'ad_id', 'ads']

    def create(self, validated_data):
        user_id = validated_data['user_id']
        ad_id = validated_data['ad_id']

        # Получаем объекты пользователя и объявления
        favorite, _ = Favorite.objects.get_or_create(user_id=user_id)
        ad = Ad.objects.get(id=ad_id)

        # Добавляем объявление в избранное
        favorite.ads.add(ad)
        return favorite

    def update(self, instance, validated_data):
        ad_id = validated_data['ad_id']
        ad = Ad.objects.get(id=ad_id)

        # Обновляем список объявлений (добавляем новое объявление)
        instance.ads.add(ad)
        instance.save()
        return instance


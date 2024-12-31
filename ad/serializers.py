from rest_framework import serializers
from .models import AdImage, Ad, AdLike
from category.serializers import CategorySerializer


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = '__all__'

class AdSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = AdImageSerializer(many=True) # добавляем к продукту массив изображений
    likes = serializers.IntegerField(read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()  # Для отображения, поставил ли лайк текущий пользователь
    class Meta:
        model = Ad
        fields = '__all__'

    def get_is_liked_by_user(self, obj):
        """
        Проверяем, поставил ли лайк текущий пользователь.
        Мы используем IP-адрес для идентификации пользователя.
        """
        request = self.context.get('request')
        if request and request.META.get('REMOTE_ADDR'):
            ip_address = request.META.get('REMOTE_ADDR')
            # Проверяем, есть ли запись о лайке для данного IP
            return AdLike.objects.filter(ad=obj, ip_address=ip_address).exists()
        return False
from rest_framework import serializers
from .models import User
from favorite.models import Favorite
from favorite.serializers import FavoriteSerializer

class UserSerializer(serializers.ModelSerializer):
    favorite = FavoriteSerializer(read_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'avatar', 'is_active', 'role', 'created_at', 'updated_at', 'favorites')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None) # удаляем после валидации
        password = validated_data.pop('password', None) # хешируем пароль, а исходный удаляем
        instance = self.Meta.model(**validated_data) # Передаем данные в конструктор модели указанный в Meta, то есть юзеру
        if password is not None: # проверка, если пароль был передан в исходном виде, хешируем его перед сохранением
            instance.set_password(password)
        instance.save() # сохраняем обьекто модели в БД


        if not hasattr(instance, 'favorites'):
            instance.favorites = Favorite.objects.create(user=instance)
            instance.save()

        return instance # возвращаем обьекто модели


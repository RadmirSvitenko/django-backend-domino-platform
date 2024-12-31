from .models import Category, Subcategory
from rest_framework import serializers




class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


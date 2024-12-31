import django_filters
from .models import Category, Subcategory
class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name', 'slug']
class SubcategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Subcategory
        fields = ['name', 'slug']

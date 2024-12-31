import django_filters
from .models import Ad
class AdFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Минимальная цена')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Максимальная цена')
    class Meta:
        model = Ad
        fields = ['name', 'category', 'slug', 'views', 'created_at', 'updated_at']


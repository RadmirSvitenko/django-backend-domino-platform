from rest_framework import viewsets, filters
from .models import Category, Subcategory
from django_filters import rest_framework as dj_filters
from .serializers import CategorySerializer, SubcategorySerializer
from .filters import CategoryFilter, SubcategoryFilter
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (dj_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = CategoryFilter
    search_fields = ['name']


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    filter_backends = (dj_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = SubcategoryFilter
    search_fields = ['name']

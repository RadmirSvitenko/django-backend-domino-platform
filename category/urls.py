from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, SubcategoryViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'subcategory', SubcategoryViewSet)

app_name = 'category'

urlpatterns = [
    path('', include(router.urls))
]
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FavoriteViewSet

app_name = 'favorite'

router = DefaultRouter()
router.register(r'favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls))
]
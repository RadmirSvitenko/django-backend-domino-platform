from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AdViewSet

router = DefaultRouter()
router.register(r'ad', AdViewSet)

app_name = 'ad'

urlpatterns = [
    path('', include(router.urls)),
]

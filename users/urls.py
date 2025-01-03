from django.contrib import admin
from django.urls import path
from .views import RegisterApiView, LoginApiView, UserApiView, LogoutApiView

app_name = 'users'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign-up/', RegisterApiView.as_view()),
    path('sign-in/', LoginApiView.as_view()),
    path('user/', UserApiView.as_view()),
    path('logout/', LogoutApiView.as_view())
]

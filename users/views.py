from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from favorite.serializers import FavoriteSerializer
from .models import User
import jwt, datetime
import environ

env = environ.Env()
env.read_env('.env')


class RegisterApiView(APIView):

    @extend_schema(
        request=UserSerializer,  # Используем сериализатор для отображения входных данных
        responses={201: UserSerializer},  # Ответ также будет сериализатором
        description="Регистрация нового пользователя"
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApiView(APIView):

    @extend_schema(
        request=UserSerializer,  # Входные данные
        responses={
            200: OpenApiParameter(
                "access_token",
                str,
                description="JWT Access Token",
            ),
            401: "Authentication Failed",
        },
        description="Авторизация пользователя",
    )
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password!')

        # Преобразуем datetime объекты в строку
        access_exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)  # Access токен 15 минут
        refresh_exp_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Refresh токен 7 дней
        iat_time = datetime.datetime.utcnow()

        access_payload = {
            'id': user.id,
            'exp': access_exp_time,
            'iat': iat_time
        }

        refresh_payload = {
            'id': user.id,
            'exp': refresh_exp_time,
            'iat': iat_time
        }

        access_token = jwt.encode(access_payload, env('SECRET_ACCESS_JWT'), algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, env('SECRET_REFRESH_JWT'), algorithm='HS256')
        response = Response()

        response.set_cookie('access_jwt', value=access_token, httponly=True)
        response.set_cookie('refresh_jwt', value=refresh_token, httponly=True)

        # Получаем связанные данные (избранное пользователя)
        favorite = user.favorite  # В случае OneToOneField, можно обращаться напрямую
        favorites_data = FavoriteSerializer(favorite).data if favorite else None

        response.data = {
            'message': 'success',
            'id': user.id,
            'name': user.username,
            'email': user.email,
            'favorites': favorites_data,
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return response


class UserApiView(APIView):

    @extend_schema(
        responses={200: UserSerializer},
        description="Получение информации о текущем пользователе",
    )
    def get(self, request):
        access_token = request.COOKIES.get('access_jwt')

        if not access_token:
            raise AuthenticationFailed('Unauthorized!')

        try:
            payload = jwt.decode(access_token, env('SECRET_ACCESS_JWT'), options={"require": ["exp"]},
                                 algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthorized!')

        user = User.objects.filter(id=payload['id']).first()  # first = search by unique field
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutApiView(APIView):

    @extend_schema(
        request=None,
        responses={200: "Logout successful"},
        description="Выход пользователя",
    )
    def post(self, request):
        response = Response()
        response.delete_cookie('access_jwt')
        response.delete_cookie('refresh_jwt')
        response.data = {
            'message': 'success'
        }

        return response

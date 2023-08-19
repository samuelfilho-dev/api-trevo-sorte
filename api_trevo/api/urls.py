from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from api import views

urlpatterns = [
    path('', views.get_routes, name='get_routes'),
    path('users', views.create_get_users, name='create_get_users'),
    path('users/<int:user_id>', views.get_update_delete_user, name='get_update_delete_user'),

    path('auth/token', TokenObtainPairView.as_view(), name='generate_token'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='verify_token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='refresh_token'),

    path('raffles/<int:combo_number>', views.combo_number, name='combo_number')
]

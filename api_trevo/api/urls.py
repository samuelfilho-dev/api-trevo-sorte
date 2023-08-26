from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from api import views

urlpatterns = [
    path('', views.get_routes, name='get_routes'),
    path('users', views.create_get_users, name='create_get_users'),
    path('users/<int:user_id>', views.get_update_delete_user, name='get_update_delete_user'),
    path('users/confrim/mail/<str:token>', views.confirm_mail_view, name='confirm_mail'),

    path('administrators', views.create_get_admin_view, name='create_get_admin_view'),
    path('administrators/<int:admin_id>', views.get_update_delete_admin, name='get_update_delete_admin'),

    path('users/email/', views.pending_email_confirm, name='pending_email_confirm'),

    path('user/raffles', views.raffle_view, name='raffle_view'),

    path('webhooks', views.confirm_webhook, name='confirm_webhook'),

    path('auth/token', TokenObtainPairView.as_view(), name='generate_token'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='verify_token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='refresh_token'),

    path('raffles/<int:combo_number>', views.generate_combo_number, name='combo_number')
]

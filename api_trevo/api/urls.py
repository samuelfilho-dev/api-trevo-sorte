from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from api import views

urlpatterns = [
    path('', views.get_routes, name='get_routes'),
    path('users', views.create_get_users, name='create_get_users'),
    path('users/<int:user_id>', views.get_update_delete_user, name='get_update_delete_user'),
    path('users/number/raffles', views.get_user_raffles_number_view, name='get_user_raffles_number_view'),
    path('users/confrim/mail/<str:token>', views.confirm_mail_view, name='confirm_mail'),

    path('users/email/', views.pending_email_confirm, name='pending_email_confirm'),

    path('user/raffles', views.raffle_view, name='raffle_view'),

    path('payments/approved', views.get_approved_payment_view, name='get_approved_payment_view'),
    path('payments/purchase/numbers', views.get_purchase_numbers_view, name='get_purchase_numbers_view'),
    path('payments/pendding/numbers', views.get_pending_numbers_view, name='get_pending_numbers_view'),

    path('administrators', views.create_get_admin_view, name='create_get_admin_view'),
    path('administrators/<int:admin_id>', views.get_update_delete_admin, name='get_update_delete_admin'),

    path('webhooks', views.confirm_webhook, name='confirm_webhook'),

    path('auth/token', TokenObtainPairView.as_view(), name='generate_token'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='verify_token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='refresh_token'),

    path('raffles/<int:combo_number>', views.generate_combo_number, name='combo_number')
]

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path, re_path
from api import views
from api.swagger_view import schema_view

urlpatterns = [
    path('users', views.create_get_users, name='Create or List Users'),
    path('users/<int:user_id>', views.get_update_delete_user, name='Get,Update or Delete User By Id'),
    path('users/number/raffles', views.get_user_raffles_number_view, name='get_user_raffles_number_view'),
    path('users/confrim/mail/<str:token>', views.confirm_mail_view, name='confirm_mail'),

    path('users/email/', views.pending_email_confirm, name='Confirm Email'),

    path('user/raffles', views.raffle_view, name='View User Info By Token'),

    path('payments/approved', views.get_approved_payment_view, name='Get Payment has Approved Status'),
    path('payments/purchase/numbers', views.get_purchase_numbers_view, name='Get Purchase Numbers List'),
    path('payments/pendding/numbers', views.get_pending_numbers_view, name='Get Pending Numbers List'),

    path('administrators', views.create_get_admin_view, name='Crate Or List Administrators'),
    path('administrators/<int:admin_id>', views.get_update_delete_admin,
         name='Get,Update or Delete Administrators By Id'),

    path('webhooks', views.confirm_webhook, name='Webhook'),

    path('auth/token', TokenObtainPairView.as_view(), name='Generate JWT Token'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='Verify JWT Token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='Refresh JWT Token'),

    path('raffles/<int:combo_number>', views.generate_combo_number, name='Generate a Raffle Ticket Number'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

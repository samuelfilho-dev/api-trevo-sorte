from django.urls import path
from api import views

urlpatterns = [
    path('', views.get_routes, name='get_routes'),
    path('users', views.create_get_users, name='create_get_users'),
    path('users/<int:user_id>', views.get_update_delete_user, name='get_update_delete_user'),

    path('raffles/<int:combo_number>', views.combo_number, name='combo_number')
]

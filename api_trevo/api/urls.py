from django.urls import path
from api import views

urlpatterns = [
    path('', views.get_routes, name='get_routes'),
    path('users', views.get_users, name='get_users'),
    path('users/create', views.create_user, name='create_user'),
    path('users/<int:user_id>', views.get_user, name='get_user'),
    path('users/<int:user_id>/update', views.update_user, name='get_user'),
    path('users/<int:user_id>/delete', views.delete_user, name='get_user'),

    path('raffles/<int:combo_number>', views.create_raffles_combo_number, name='create_raffles_combo_number')
]

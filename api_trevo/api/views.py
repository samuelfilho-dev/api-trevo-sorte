from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from .utils import create_user
from .utils import get_users
from .utils import get_user
from .utils import update_user
from .utils import delete_user
from .utils import create_raffles_combo_number


@api_view(['GET'])
def get_routes(request):
    routes = [
        '',
        'tickets/',
        'tickets/<id>',
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
def create_get_users(request):
    user = request.user

    if request.method == 'GET':
        # if not user.role == 'admin':
        #     return Response({'message': 'This User is not Authenticate', 'datetime': datetime.now()},
        #                     status=status.HTTP_403_FORBIDDEN)
        response = get_users()
        return Response(response.data)
    if request.method == 'POST':
        response = create_user(request)
        return Response(response.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_update_delete_user(request, user_id):
    user = request
    if request.method == 'GET':
        # if not user.role == 'admin':
        #     return Response({'message': 'This User is not Authenticate', 'datetime': datetime.now()},
        #                     status=status.HTTP_403_FORBIDDEN)
        response = get_user(request, user_id)
        return Response(response.data)
    if request.method == 'PUT':
        update_user(request, user_id)
        response = update_user(request, user_id)
        return Response(response.data)
    if request.method == 'DELETE':
        # if not user.role == 'admin':
        #     return Response({'message': 'This User is not Authenticate', 'datetime': datetime.now()},
        #                     status=status.HTTP_403_FORBIDDEN)
        delete_user(request, user_id)
        return Response('', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def combo_number(request):
    if request.GET:
        raffles_combo_number = create_raffles_combo_number(request, combo_number)
        return Response(raffles_combo_number)

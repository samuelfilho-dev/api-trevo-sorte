from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .token_utils import decode_token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .utils import create_user
from .utils import get_users
from .utils import get_user
from .utils import update_user
from .utils import delete_user
from .utils import create_raffles_combo_number
from datetime import datetime


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email
        token['role'] = user.role

        return token


@api_view(['GET'])
def get_routes(request):
    routes = [
        """
        /users
        /users/{id}, 

        /auth/token
        /auth/token/verify
        /auth/token/refresh

        /raffles/<int:combo_number>'
        """
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
def create_get_users(request):
    access = None

    if 'Authorization' in request.headers:
        header_token = request.headers['Authorization']
        token = get_token(header_token)
        access = verify_user(token)

    if request.method == 'GET':
        if access:
            response = get_users()
            return Response(response.data)
        else:
            return Response({'message': 'This User is not Authenticate', 'timestamp': datetime.now()},
                            status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        response = create_user(request)
        return Response(response.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_update_delete_user(request, user_id):
    access = None

    if 'Authorization' in request.headers:
        header_token = request.headers['Authorization']
        token = get_token(header_token)
        access = verify_user(token)

    if request.method == 'GET':
        if access:
            response = get_user(request, user_id)
            return Response(response.data)
        else:
            return Response({'message': 'This User is not Authenticate', 'timestamp': datetime.now()},
                            status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        update_user(request, user_id)
        response = update_user(request, user_id)
        return Response(response.data)

    if request.method == 'DELETE':
        delete_user(request, user_id)
        return Response('', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def generate_combo_number(request, combo_number):
    if request.method == 'GET':
        raffles_combo_number = create_raffles_combo_number(combo_number)
        return Response(raffles_combo_number)


def get_token(header_token):
    if header_token.startswith('Bearer '):
        token = header_token.split(' ')[1]
        return token
    else:
        return {'message': 'Failed a Decoded Token', 'timestamp': datetime.now()}


def verify_user(token):
    payload = decode_token(token)

    if payload['role'] == 'admin':
        return True
    else:
        return False

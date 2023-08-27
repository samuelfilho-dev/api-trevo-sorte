from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .token_utils import decode_token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .mp_service import confirm_payment
from .utils import create_user
from .utils import get_users
from .utils import get_user
from .utils import create_admin_user
from .utils import get_admin_users
from .utils import get_admin
from .utils import update_admin
from .utils import delete_admin
from .utils import get_pending_email
from .utils import get_raffle
from .utils import update_user
from .utils import delete_user
from .utils import confirm_mail
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
        """/users/users/{id},\n\n/auth/token/auth/token/verify/auth/token/refresh\n/raffles/<int:combo_number>'
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
@permission_classes([IsAuthenticated])
def get_update_delete_user(request, user_id):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    access = verify_user(token)

    if request.method == 'GET':
        response = get_user(user_id)
        return Response(response.data)

    if request.method == 'PUT':
        response = update_user(request, user_id)
        return Response(response.data)

    if request.method == 'DELETE':
        delete_user(user_id)
        return Response('', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_get_admin_view(request):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    access = verify_user(token)

    if not access:
        Response({'message': 'This User is not Authenticate', 'timestamp': datetime.now()},
                 status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        response = get_admin_users()
        return Response(response.data)

    if request.method == 'POST':
        response = create_admin_user(request)
        return Response(response.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete_admin(request, admin_id):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    access = verify_user(token)

    if not access:
        return Response({'message': 'This User is not Authenticate', 'timestamp': datetime.now()},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        response = get_admin(admin_id)
        return Response(response.data)

    if request.method == 'PUT':
        response = update_admin(request, admin_id)
        return Response(response.data)

    if request.method == 'DELETE':
        delete_admin(admin_id)
        return Response('', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def pending_email_confirm(request):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    access = verify_user(token)

    if access:
        users = get_pending_email()
        return Response(users)
    else:
        return Response({'message': 'This User is not Authenticate', 'timestamp': datetime.now()},
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def raffle_view(request):
    user = request.user
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    username = get_username(token)

    raffles = get_raffle(email=username)

    return Response(raffles)


@api_view(['GET'])
def confirm_mail_view(request, token):
    response = confirm_mail(key=token)
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def generate_combo_number(request, combo_number):
    if request.method == 'GET':
        raffles_combo_number = create_raffles_combo_number(combo_number)
        return Response(raffles_combo_number)


@api_view(['POST'])
def confirm_webhook(request):
    print(request.data)

    data = request.data
    if 'resource' in data:
        link = data['resource']
        confirm_payment(payment_link=link)

    return Response('', status=status.HTTP_200_OK)


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


def get_username(token):
    payload = decode_token(token)
    return payload['email']

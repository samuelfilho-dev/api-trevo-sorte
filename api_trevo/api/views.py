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
from .utils import get_approved_payment
from .utils import get_purchase_numbers
from .utils import create_raffles_combo_number
from .utils import get_user_raffles_number
from .utils import get_pending_numbers
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email
        token['role'] = user.role

        return token


@swagger_auto_schema(
    methods=['GET'],
    operation_description="List All Users",
    responses={200: 'List Users', 401: 'Unauthorized', 403: 'Has no authority'},
)
@swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='User Name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone Number'),
            'combo_number': openapi.Schema(type=openapi.TYPE_STRING, description='Number of Purchase\'s Combo'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User Password')
        },
        required=['name', 'email', 'phone', 'combo_number', 'password'],
    ),
    operation_description='Crate User With a Payment and Raffle List',
    responses={201: 'User Created Success', 400: 'Bad Request', 422: 'Invalid Entity'},
)
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


@swagger_auto_schema(
    methods=['GET'],
    operation_description="Get User By Id",
    responses={200: 'Get User', 401: 'Unauthorized', 403: 'Has no authority'},
)
@swagger_auto_schema(
    methods=['PUT'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='User Name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone Number'),
        },
        required=['name', 'email', 'phone'],
    ),
    operation_description='Update User By Id',
    responses={200: 'User Updated Success', 400: 'Bad Request', 422: 'Invalid Entity', 401: 'Unauthorized',
               403: 'Has no authority'},
)
@swagger_auto_schema(
    methods=['DELETE'],
    operation_description='Delete User By Id',
    responses={204: 'No Content, User Deleted Success', 400: 'Bad Request', 401: 'Unauthorized',
               403: 'Has no authority'}
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete_user(request, user_id):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    access = verify_user(token)

    if not access:
        Response({'message': 'This User is not Authenticate', 'timestamp': datetime.now()},
                 status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        response = get_user(user_id)
        return Response(response.data)

    if request.method == 'PUT':
        response = update_user(request, user_id)
        return Response(response.data)

    if request.method == 'DELETE':
        delete_user(user_id)
        return Response('', status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    methods=['GET'],
    operation_description="List All Administrators",
    responses={200: 'List Users', 401: 'Unauthorized', 403: 'Has no authority'},
)
@swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='User Name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone Number'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User Password')
        },
        required=['name', 'email', 'phone', 'password'],
    ),
    operation_description='Crate API\'s Administrator',
    responses={201: 'Administrator Created Success', 400: 'Bad Request', 422: 'Invalid Entity'},
)
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


@swagger_auto_schema(
    methods=['GET'],
    operation_description="Get Administrator By Id",
    responses={200: 'Get Administrator', 401: 'Unauthorized', 403: 'Has no authority'},
)
@swagger_auto_schema(
    methods=['PUT'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='User Name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone Number'),
        },
        required=['name', 'email', 'phone'],
    ),
    operation_description='Update Administrator By Id',
    responses={200: 'Administrator Updated Success', 400: 'Bad Request', 422: 'Invalid Entity'},
)
@swagger_auto_schema(
    methods=['DELETE'],
    operation_description='Delete Administrator By Id',
    responses={204: 'No Content, Administrator Deleted Success', 400: 'Bad Request', 422: 'Invalid Entity'}
)
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


@swagger_auto_schema(
    method='GET',
    operation_description='List Users With a E-mail Pending',
    responses={200: 'List Users', 401: 'Unauthorized', 403: 'Has no authority'}
)
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


@swagger_auto_schema(
    method='GET',
    operation_description='Get Information User By JWT Token',
    responses={200: 'Get User Information', 401: 'Unauthorized', 403: 'Has no authority'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def raffle_view(request):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    username = get_username(token)

    raffles = get_raffle(email=username)

    return Response(raffles)


@swagger_auto_schema(
    method='GET',
    operation_description='Get User Number List By JWT Token',
    responses={200: 'Get User Information', 401: 'Unauthorized', 403: 'Has no authority'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_raffles_number_view(request):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    username = get_username(token)

    raffle = get_user_raffles_number(email=username)
    return Response(raffle)


@swagger_auto_schema(
    method='GET',
    operation_description='List Payment has Status Approved',
    responses={200: 'List Payments', 401: 'Unauthorized', 403: 'Has no authority'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_approved_payment_view(request):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    access = verify_user(token)

    if not access:
        return Response({'message': 'This User is not Authenticate', 'timestamp': datetime.now()},
                        status=status.HTTP_403_FORBIDDEN)

    response = get_approved_payment()
    return Response(response.data)


@swagger_auto_schema(
    method='GET',
    operation_description='Get Purchase Number List',
    responses={200: 'List Purchase Number List'}
)
@api_view(['GET'])
def get_purchase_numbers_view(request):
    response = get_purchase_numbers()
    return Response(response.data)


@swagger_auto_schema(
    method='GET',
    operation_description='Get Pending Number List',
    responses={200: 'List Pending Number List', 401: 'Unauthorized', 403: 'Has no authority'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_numbers_view(request):
    header_token = request.headers['Authorization']
    token = get_token(header_token)
    access = verify_user(token)

    if not access:
        return Response({'message': 'This User is not Authenticate', 'timestamp': datetime.now()},
                        status=status.HTTP_403_FORBIDDEN)

    response = get_pending_numbers()
    return Response(response.data)


@swagger_auto_schema(
    method='GET',
    operation_description='Confirm Email By User\'s Key',
    responses={200: 'Email was Confirm', 400: 'Email was not Confirm'}
)
@api_view(['GET'])
def confirm_mail_view(request, token):
    response = confirm_mail(key=token)
    return Response(response)


@swagger_auto_schema(
    method='GET',
    operation_description='Generate Raffles Ticket\'s Numbers With Combo Number',
    responses={200: 'List Created'}
)
@api_view(['GET'])
def generate_combo_number(request, combo_number):
    if request.method == 'GET':
        raffles_combo_number = create_raffles_combo_number(combo_number)
        return Response(raffles_combo_number)


@swagger_auto_schema(
    method='POST',
    operation_description='Confirm Payment Webhook',
    responses={200: 'Confirmed recipient'}
)
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

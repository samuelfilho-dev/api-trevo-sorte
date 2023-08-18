from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UserModel
from .models import Payment
from .serializer import UserModelSerializer
from .mp_service import generate_payment

import numpy as np

# Create your views here.

@api_view(['GET'])
def get_routes(request):
    routes = [
        '',
        'tickets/',
        'tickets/<id>',
    ]
    return Response(routes, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_users(request):
    users = UserModel.objects.all()
    serializer = UserModelSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user(request, user_id):
    user = UserModel.objects.get(id=user_id)
    serializer = UserModelSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_user(request, user_id):
    user = UserModel.objects.get(id=user_id)
    data = request.data

    seralizer = UserModelSerializer(instance=user, data=data)

    if seralizer.is_valid():
        seralizer.save()

    return Response(seralizer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request, user_id):
    user = UserModel.objects.get(id=user_id)
    user.delete()
    return Response('', status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_user(request):
    data = request.data

    name = data['name']
    email = data['email']
    phone = data['phone']
    password = data['password']

    new_user = UserModel.objects.create(
        name=name,
        email=email,
        phone=phone,
        password=password,
    )

    payment = create_payment(email=email, value=0.01, user=new_user)

    serializer = UserModelSerializer(new_user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def create_payment(value, email, user):
    data_payment = generate_payment(
        value=value,
        email=email
    )

    new_payment = Payment.objects.create(
        status=data_payment['status'],
        api_id=data_payment['id'],
        value=data_payment['transaction_amount'],
        qr_code=data_payment['point_of_interaction']['transaction_data']['qr_code'],
        qr_code_base64=data_payment['point_of_interaction']['transaction_data']['qr_code_base64'],
        date_expiration=data_payment['date_of_expiration'],
        user_id=user.id
    )

    return new_payment


def create_raffle(request):
    raflle = [raffle for raffle in range(100_001)]
    # Add Filter Rules

    return Response(raflle, status=status.HTTP_200_OK)

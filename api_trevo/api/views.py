from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UserModel
from .models import Payment
from .models import RaffleTicket
from .serializer import UserModelSerializer
from .mp_service import generate_payment
from datetime import datetime

import numpy as np


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
    combo_number = data['combo_number']

    value = get_value(combo_number)

    new_user = UserModel.objects.create(
        name=name,
        email=email,
        phone=phone,
        password=password,
    )

    create_payment(email=email, value=value, user=new_user)

    raffles_combo_number = create_combo_number(combo_number=combo_number)
    crate_raffle_ticket(combo_number=combo_number, raffles_combo_number=raffles_combo_number, user=new_user)

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


@api_view(['GET'])
def create_raffles_combo_number(request, combo_number):
    raffles_combo_number = create_combo_number(combo_number)
    return Response(raffles_combo_number, status=status.HTTP_200_OK)


def crate_raffle_ticket(combo_number, raffles_combo_number, user):
    new_raffle_ticket = RaffleTicket.objects.create(
        combo_name=f'Combo: {combo_number}',
        combo_number=combo_number,
        raffle=raffles_combo_number,
        user_id=user.id
    )

    return new_raffle_ticket


def create_combo_number(combo_number):
    raffles = [raffle for raffle in range(100_001)]
    # Add Filter Rules

    if combo_number not in [5, 10, 15, 30, 50, 100]:
        return Response({'message:': 'This Combo Number is not exists', 'datetime': datetime.now()},
                        status=status.HTTP_400_BAD_REQUEST)

    raffles_combo_number = np.random.choice(raffles, combo_number)

    return raffles_combo_number


def get_value(combo_number):
    value = 0
    if combo_number == 5:
        value = 2.45
        return value
    elif combo_number == 10:
        value = 4.90
        return value
    elif combo_number == 15:
        value = 7.35
        return value
    elif combo_number == 30:
        value = 14.70
        return value
    elif combo_number == 50:
        value = 24.50
        return value
    elif combo_number == 100:
        value = 49.00
        return value
    else:
        return Response({'message': 'The price of combo is not exists', 'datetime': datetime.now},
                        status=status.HTTP_400_BAD_REQUEST)

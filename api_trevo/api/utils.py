from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import transaction
from .models import UserModel
from .models import Payment
from .models import RaffleTicket
from .serializer import UserModelSerializer
from .serializer import RaffleTicketSerializer
from .mp_service import generate_payment
from datetime import datetime

import numpy as np
import uuid


def get_users():
    users = UserModel.objects.filter(status='active')
    serializer = UserModelSerializer(users, many=True)
    return serializer


@transaction.atomic
def create_user(request):
    data = request.data

    name = data['name']
    email = data['email']
    phone = data['phone']
    password = data['password']
    role = data['role']
    combo_number = data['combo_number']

    new_user = UserModel.objects.create(
        name=name,
        email=email,
        phone=phone,
        password=password,
        role=role
    )

    key = generate_confirm_key()

    new_user.set_password(password)
    new_user.key = key
    new_user.save()

    if new_user.role == 'admin':
        new_user.raffles = None
        serializer = UserModelSerializer(new_user)
        return serializer

    raffles_combo_number = create_combo_number(combo_number=combo_number)
    crate_raffle_ticket(combo_number=combo_number, raffles_combo_number=raffles_combo_number, user=new_user,
                        email=email)

    generate_email(email=email, user=new_user, key=key)

    serializer = UserModelSerializer(new_user)
    return serializer


@transaction.atomic
def crate_raffle_ticket(email, combo_number, raffles_combo_number, user):
    value = get_value(combo_number)
    payment = create_payment(email=email, value=value)

    new_raffle_ticket = RaffleTicket.objects.create(
        combo_name=f'Combo Do {user.name} - {combo_number} Números',
        combo_number=combo_number,
        raffle=raffles_combo_number,
        user_id=user.id,
        payment_id=payment.id
    )

    return new_raffle_ticket


@transaction.atomic
def create_payment(value, email):
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
        url=data_payment['point_of_interaction']['transaction_data']['ticket_url'],
        date_expiration=data_payment['date_of_expiration'],
    )

    return new_payment


def create_combo_number(combo_number):
    raffles = [raffle for raffle in range(100_001)]
    # Add Filter Rules

    if combo_number not in [5, 10, 15, 30, 50, 100]:
        return {'message:': 'This Combo Number do not exists', 'timestamp': datetime.now()},

    raffles_combo_number = np.random.choice(raffles, combo_number)

    return raffles_combo_number


def get_user(user_id):
    user = UserModel.objects.get(id=user_id)
    serializer = UserModelSerializer(user)
    return serializer


def get_raffle(email):
    try:
        user = UserModel.objects.get(email=email)
        serializer = RaffleTicketSerializer(user.raffles, many=True)
        return serializer.data
    except ObjectDoesNotExist:
        return {'message': 'This email do not exists', 'timestamp': datetime.now()}


def get_pending_email():
    try:
        users = UserModel.objects.filter(status='pending')
        serializer = UserModelSerializer(users, many=True)
        return serializer.data
    except ObjectDoesNotExist:
        return {'message': 'This Status do not exists', 'timestamp': datetime.now()}


def create_raffles_combo_number(combo_number):
    raffles_combo_number = create_combo_number(combo_number)
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
        return {'message': 'The price of combo is not exists', 'timestamp': datetime.now()}


def update_user(request, user_id):
    user = UserModel.objects.get(id=user_id)
    data = request.data

    serializer = UserModelSerializer(instance=user, data=data)

    if serializer.is_valid():
        serializer.save()

    return serializer


def delete_user(user_id):
    user = UserModel.objects.get(id=user_id)
    raffle = RaffleTicket.objects.get(user_id=user.id)
    payment = Payment.objects.get(raffleticket=raffle.id)

    user.status = 'disabled'
    raffle.status = 'disabled'
    payment.status = 'disabled'

    user.save()
    raffle.save()
    payment.save()


def generate_confirm_key():
    return uuid.uuid4().hex


def confirm_mail(key):
    status = 'active'

    try:
        user = UserModel.objects.get(key=key)
        user.status = status
        user.is_active = True
        user.save()
        return {'message': 'The user were confirmed', 'timestamp': datetime.now()}
    except ObjectDoesNotExist:
        return {'message': 'Email Not Confirmed', 'timestamp': datetime.now()}


def generate_email(email, user, key):
    subject = 'Api-Trevo: Confrimar E-mail'
    message = f"""Prezado(a) {user.name} 
    
    Agradecemos a sua solicitação de cadastramento em nosso site!
    Para que possamos liberar o seu cadastro em nosso sistema, solicitamos a 
    confirmação de e-mail clickcando no link abaixo:
    
    http://localhost:8000/api/users/confrim/mail/{key}
    
    Está mensagem foi enviada a você pela empresa XXX.
    Você está recebendo da empresa XXX, porque está cadastro no nosso sistema.
    Nenhum e-mail enviado pela empresa XXX tem arquivos anexados ou solicita o preechimento 
    de senhas e informações cadastrais.
    
    
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )

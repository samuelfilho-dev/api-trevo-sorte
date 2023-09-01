from django.conf import settings
from .models import Payment
from .models import RaffleTicket
from .models import NumberList

import mercadopago
import requests

sdk = mercadopago.SDK(settings.TOKEN_MERCADO_PAGO)


def generate_payment(value, email):
    payment_data = {
        "transaction_amount": value,
        "payment_method_id": "pix",
        "payer": {
            "email": email,
        },

    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    return payment


def confirm_payment(payment_link):
    headers = {
        "Authorization": f"Bearer {settings.TOKEN_MERCADO_PAGO}"
    }

    response = requests.get(payment_link, headers=headers)
    data = response.json()

    payment_id = data['collection']['id']
    payment = Payment.objects.get(api_id=payment_id)
    raffle_ticket = RaffleTicket.objects.get(id=payment.raffleticket.id)

    api_status = data['collection']['status']

    if api_status == 'approved':
        payment.status = api_status
        payment.save()

        number_list = NumberList.objects.get(id=1)

        if number_list.purchase_list is None:
            number_list.purchase_list = list(raffle_ticket.raffle)
        else:
            list_raffle_ticket = list(raffle_ticket.raffle)
            number_list.purchase_list.extend(list_raffle_ticket)

        number_list.save()

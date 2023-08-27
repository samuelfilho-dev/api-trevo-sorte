from django.conf import settings
from .models import Payment

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
        "notification_url": f"{settings.WEBHOOK_MERCADO_PAGO}"
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

    payment.status = data['collection']['status']
    payment.save()

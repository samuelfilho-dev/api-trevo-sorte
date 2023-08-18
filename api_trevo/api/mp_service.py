from django.conf import settings

import mercadopago

sdk = mercadopago.SDK(settings.TOKEN_MERCADO_PAGO)


def generate_payment(value, email):
    payment_data = {
        "transaction_amount": value,
        "payment_method_id": "pix",
        "payer": {
            "email": email,
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    return payment

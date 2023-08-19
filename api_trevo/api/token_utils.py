from django.conf import settings
from datetime import datetime
import jwt


def decode_token(token):
    try:
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return {'message': 'Expired Token', 'timestamp': datetime.now()}
    except jwt.InvalidTokenError:
        return {'message': 'Token Invalid', 'timestamp': datetime.now()}

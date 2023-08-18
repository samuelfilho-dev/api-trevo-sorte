from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserModel
from .models import Payment
from .models import RaffleTicket


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class RaffleTicketSerializer(ModelSerializer):

    class Meta:
        model = RaffleTicket
        fields = '__all__'


class UserModelSerializer(ModelSerializer):
    payment = PaymentSerializer()
    raffles = RaffleTicketSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'name', 'email', 'phone', 'role', 'create_at', 'update_at', 'payment', 'raffles']

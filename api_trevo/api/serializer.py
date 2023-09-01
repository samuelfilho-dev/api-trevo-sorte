from rest_framework.serializers import ModelSerializer
from .models import UserModel
from .models import Payment
from .models import RaffleTicket
from .models import NumberList


class NumberPurchaseListSerializer(ModelSerializer):
    class Meta:
        model = NumberList
        fields = ['purchase_list']


class NumberPendingListSerializer(ModelSerializer):
    class Meta:
        model = NumberList
        fields = ['pending_number_list']


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class RaffleTicketSerializer(ModelSerializer):
    payment = PaymentSerializer()

    class Meta:
        model = RaffleTicket
        fields = '__all__'


class RaffleTicketListSerializer(ModelSerializer):
    class Meta:
        model = RaffleTicket
        fields = ['raffle']


class UserModelSerializer(ModelSerializer):
    raffles = RaffleTicketSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'name', 'email', 'phone', 'role', 'status', 'create_at', 'update_at', 'raffles']

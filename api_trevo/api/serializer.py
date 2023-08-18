from rest_framework.serializers import ModelSerializer
from .models import UserModel
from .models import Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserModelSerializer(ModelSerializer):
    payment = PaymentSerializer()

    class Meta:
        model = UserModel
        fields = ['id','name', 'email', 'phone', 'role', 'create_at', 'update_at', 'payment']

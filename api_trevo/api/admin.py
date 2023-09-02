from django.contrib import admin
from .models import UserModel
from .models import RaffleTicket
from .models import Payment
from .models import NumberList

# Register your models here.

admin.site.register(UserModel)
admin.site.register(RaffleTicket)
admin.site.register(Payment)
admin.site.register(NumberList)

from django.contrib import admin
from .models import UserModel
from .models import RaffleTicket
from .models import Payment

# Register your models here.

admin.site.register(UserModel)
admin.site.register(RaffleTicket)
admin.site.register(Payment)



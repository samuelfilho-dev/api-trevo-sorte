from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, name, phone, role, email, password, **extra_fields):
        if not email:
            raise ValueError('E-mail is required')
        email = self.normalize_email(email)
        user = self.model(name=name, phone=phone, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, phone, role, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')
        return self.create_user(name=name, phone=phone, role=role, email=email, password=password, **extra_fields)


class UserModel(AbstractBaseUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default='pending')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    key = models.CharField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True


class RaffleTicket(models.Model):
    status = models.CharField(max_length=10, default='active')
    combo_name = models.CharField(max_length=120)
    combo_number = models.IntegerField()
    raffle = ArrayField(models.IntegerField(), blank=True, null=True)
    payment = models.OneToOneField('Payment', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('UserModel', on_delete=models.DO_NOTHING, related_name='raffles')

    def __str__(self):
        return f"Raffle - {self.user.name}"

    def save(self, *args, **kwargs):
        if self.raffle is not None:
            self.raffle = list(self.raffle)
        super(RaffleTicket, self).save(*args, **kwargs)


class Payment(models.Model):
    status = models.CharField(max_length=10, default='pending')
    api_id = models.CharField(null=True)
    value = models.CharField(max_length=10, null=True)
    qr_code = models.CharField(null=True)
    qr_code_base64 = models.TextField(null=True)
    url = models.TextField(max_length=100, null=True, blank=True)
    date_expiration = models.CharField(max_length=50, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment of {self.raffleticket.user.name}"

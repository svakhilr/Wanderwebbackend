from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime
from random import randint

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    otp = models.PositiveBigIntegerField(null=True,blank=True)
    otp_added_time = models.DateTimeField(null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def update_otp(self):
        random_otp = randint(100000, 999999)
        current_time = datetime.datetime.now()
        self.otp = random_otp
        self.otp_added_time = current_time
        self.save()
        return self.otp


from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_num(value):
    if len(str(value)) != 10:
        print(len(str(value)))
        raise ValidationError(
            _('Not a Valid Phone Number')
        )

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have a phone number')
        if not password:
            raise ValueError('Users must have a Password')
        user = self.model(phone=phone)

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(phone=phone,password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = None
    phone = models.IntegerField(unique=True,validators=[validate_num],primary_key=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    objects = UserManager()




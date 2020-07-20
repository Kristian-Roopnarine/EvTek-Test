from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17) # validators should be a list
    account_type = models.ForeignKey('AccountType',on_delete=models.CASCADE,null=True)

class Address(models.Model):
    street = models.CharField(max_length = 100)
    apt = models.CharField(max_length = 100,blank=True)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(_("zip code"),max_length=5,default="34223")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.state} - {self.zipcode}"
class AccountType(models.Model):
    value = models.CharField(max_length = 200)

    def __str__(self):
        return self.value
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.

User = get_user_model()
class WasteBinType(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Notes(models.Model):

    description = models.TextField(max_length=500)

    def __str__(self):
        return self.description
        
class PickUp(models.Model):

    bin_type = models.ForeignKey(WasteBinType,on_delete=models.CASCADE)
    weight = models.FloatField()
    scheduled_user = models.ForeignKey(User,on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)
    # add notes

    def get_absolute_url(self):
        return reverse('pickup-detail',kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.scheduled_user} - {self.scheduled_date} - {self.bin_type}"


    
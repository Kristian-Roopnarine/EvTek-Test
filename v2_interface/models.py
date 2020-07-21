from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.

User = get_user_model()
class WasteBinTypeV2(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class NotesV2(models.Model):

    description = models.TextField(max_length=500)

    def __str__(self):
        return self.description
        
class PickUpV2(models.Model):

    bin_type = models.ForeignKey(WasteBinTypeV2,on_delete=models.CASCADE)
    weight = models.FloatField()
    scheduled_user = models.ForeignKey(User,on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)
    # add notes

    def get_absolute_url(self):
        return reverse('v2_interface:pickup-detail',kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.scheduled_user} - {self.scheduled_date} - {self.bin_type}"
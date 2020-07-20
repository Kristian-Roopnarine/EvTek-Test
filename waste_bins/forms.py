from .models import PickUp,Notes
from django import forms
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type="date"
    
class PickUpForm(ModelForm):

    class Meta:
        model = PickUp
        exclude=['scheduled_user']

        widgets = {
            'scheduled_date':DateInput()
        }
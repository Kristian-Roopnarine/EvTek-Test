from .models import PickUp,Notes
from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminSplitDateTime,AdminDateWidget,AdminTimeWidget

class DateInput(forms.DateInput):
    input_type="date"

class TimeInput(forms.TimeInput):
    input_type='time'

class PickUpForm(ModelForm):
    
    class Meta:
        model = PickUp
        exclude=['scheduled_user']
        widgets = {
            'scheduled_date':DateInput(),
            'scheduled_time':TimeInput()
        }
    
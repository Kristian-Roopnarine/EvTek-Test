from .models import PickUpV2,NotesV2
from django import forms
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type="date"

class PickUpForm(ModelForm):
    
    class Meta:
        model = PickUpV2
        exclude=['scheduled_user','completed']
        widgets = {
            'scheduled_date':DateInput(),
        }
    
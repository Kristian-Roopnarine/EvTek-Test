from .models import PickUpV2,NotesV2
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class DateInput(forms.DateInput):
    input_type="date"

class PickUpForm(ModelForm):
    
    class Meta:
        model = PickUpV2
        exclude=['scheduled_user','completed']
        widgets = {
            'scheduled_date':DateInput(),
        }

class RecurringPickUpForm(ModelForm):
    recurring = forms.IntegerField()
    class Meta:
        model = PickUpV2
        exclude=['scheduled_user','completed']
        widgets = {
            'scheduled_date':DateInput()
        }
        help_texts = {
            'recurring':_('How many weeks should we continue this pick up?')
        }
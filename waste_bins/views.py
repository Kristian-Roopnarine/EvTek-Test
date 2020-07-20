from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .models import PickUp,WasteBinType,Notes
from .forms import PickUpForm
# Create your views here.


# list view for scheduled pick ups

class PickUpList(LoginRequiredMixin,ListView):
    context_object_name = "user_pick_ups"

    def get_queryset(self):
        return PickUp.objects.filter(scheduled_user=self.request.user).order_by('-scheduled_date')

# create view of pickup
class PickUpCreateForm(LoginRequiredMixin,CreateView):
    form_class = PickUpForm
    success_url = reverse_lazy('waste_bins:schedule-list')
    template_name = "waste_bins/pickup_form.html"

    def form_valid(self,form):
        form.instance.scheduled_user = self.request.user
        return super(PickUpCreateForm,self).form_valid(form)

# edit view of pickup
class PickUpUpdateForm(LoginRequiredMixin,UpdateView):
    form_class = PickUpForm
    model = PickUp
    success_url = reverse_lazy('waste_bins:schedule-list')
    template_name = 'waste_bins/pickup_form.html'

# delete view of pick up

class PickUpDeleteForm(LoginRequiredMixin,DeleteView):
    model = PickUp
    success_url = reverse_lazy('waste_bins:schedule-list')
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import PickUp,WasteBinType,Notes
from .forms import PickUpForm
import datetime as dt
from django.db.models import Sum,Count
# Create your views here.

# home
@login_required()
def index(request):
    today = dt.date.today()

    # update all pick ups when user visits home page and when todays date == pick up date
    pick_up_list = PickUp.objects.filter(scheduled_user=request.user,scheduled_date__lte=today)
    print(pick_up_list)
    for pick_up in pick_up_list:
        if not pick_up.completed and pick_up.scheduled_date <= today:
            pick_up.completed = True
            pick_up.save()

    # set up notifications for pick ups
        # when pick up is tomorrow
        # when DoS picks up bin
    return render(request,'_base.html')

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

@login_required()
def dashboard(request):
    context = {}
    pick_up_list = PickUp.objects.filter(scheduled_user=request.user,completed=True).order_by('-completed')
    context['total_poundage'] = pick_up_list.values('bin_type__name').annotate(total_pounds = Sum('weight'))
    context['total_pickups'] = pick_up_list.values('bin_type__name').annotate(completed=Count('completed'))
    print(pick_up_list.values('bin_type__name','scheduled_date'))
    return render(request,'waste_bins/dashboard.html',context)

    
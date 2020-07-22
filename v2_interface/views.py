from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PickUpV2,WasteBinTypeV2,ConfirmPickUp,PickUpReminder
from .forms import PickUpForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView,UpdateView,DeleteView,CreateView
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta,date
from django.db.models import Sum,Count
from django.http import JsonResponse

from .utils import Calendar

# Create your views here.
@login_required()
def index(request):
    today = date.today()
    tomorrow = today + timedelta(1)
    context = {'notifications':[]}

    # update all pick ups when user visits home page and when todays date == pick up date
    pick_up_list = PickUpV2.objects.filter(scheduled_user=request.user,scheduled_date__lte=tomorrow)
    
    for pick_up in pick_up_list:
        if not pick_up.completed and pick_up.scheduled_date <= today:
            pick_up.completed = True
            pick_up.save()
            confirm_note = ConfirmPickUp.objects.create(description=f"Your {pick_up.bin_type.name} was picked up today!",pick_up=pick_up)
            confirm_note.save()
        if pick_up.scheduled_date == tomorrow:
            obj,created = PickUpReminder.objects.get_or_create(
                pick_up=pick_up,
                description = f"Your {pick_up.bin_type.name} will be picked up tomorrow!"
            )
    context['confirm_pickups'] = ConfirmPickUp.objects.filter(date=today,pick_up__scheduled_user=request.user)
    context['pickup_reminder'] = PickUpReminder.objects.filter(date=today,pick_up__scheduled_user=request.user)

    pick_up_list = pick_up_list.filter(completed=True).order_by('-completed')
    context['bin_type_data'] = pick_up_list.values('bin_type__name','bin_type__id').annotate(total_pounds = Sum('weight'),completed=Count('completed'))
    return render(request,'_base.html',context)

# visualiztion view
# needs to return all of the bin type names for a person in one list, then the total pounds collected for that bin


@login_required()
def bin_pound_data(request):
    completed_list = PickUpV2.objects.filter(scheduled_user=request.user,completed=True).values('bin_type__name').annotate(total_pounds=Sum('weight'))

    name_array=[]
    weight_array=[]
    for data in completed_list:
        name = data['bin_type__name']
        weight = data['total_pounds']
        name_array.append(name)
        weight_array.append(weight)
    data = {
        'labels':name_array,
        'data':weight_array
    }

    return JsonResponse(data)

class CalendarView(LoginRequiredMixin,ListView):
    model = PickUpV2
    template_name = 'v2_interface/calendar.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        # use todays date for the calendar
        d = get_date(self.request.GET.get('day',None))

        # create calendar class
        cal = Calendar(d.year,d.month)

        html_cal = cal.format_month(self.request.user,withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context
    
    def get_queryset(self,**kwargs):
        #d = get_date(self.request.GET.get('day',None))
        return PickUpV2.objects.filter(scheduled_user=self.request.user)

def get_date(req_day):
    if req_day:
        year,month = (int(x) for x in req_day.split("-"))
        return date(year,month,day=1)
    return date.today()

class PickUpCreateView(LoginRequiredMixin,CreateView):
    model = PickUpV2
    form_class = PickUpForm
    success_url = reverse_lazy('v2_interface:schedule-list')
    template_name = 'v2_interface/pickup_form.html'

    def form_valid(self,form):
        form.instance.scheduled_user = self.request.user
        return super(PickUpCreateView,self).form_valid(form)

class PickUpDetailView(LoginRequiredMixin,DetailView):
    model = PickUpV2
    template_name = 'v2_interface/pickup_detail.html'

class PickUpEditView(LoginRequiredMixin,UpdateView):
    form_class = PickUpForm
    model = PickUpV2
    template_name = 'v2_interface/pickup_form.html'

class PickUpDeleteView(LoginRequiredMixin,DeleteView):
    model = PickUpV2
    template_name = 'v2_interface/pickup_confirm_delete.html'
    success_url = reverse_lazy('v2_interface:schedule-list')


class BinPickUpDates(LoginRequiredMixin,ListView):
    template_name = "v2_interface/bin_pickup_dates.html"
    context_object_name = "bin_dates"

    def get_queryset(self,**kwargs):
        return PickUpV2.objects.filter(scheduled_user=self.request.user,bin_type__id=self.kwargs['pk'],completed=True)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        bin_type = WasteBinTypeV2.objects.get(id=self.kwargs['pk'])
        context['bin_name'] = bin_type.name
        return context
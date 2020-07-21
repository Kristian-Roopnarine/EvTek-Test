from django.shortcuts import render
from django.urls import reverse_lazy
import datetime as dt
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PickUpV2,WasteBinTypeV2
from .forms import PickUpForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView,UpdateView,DeleteView,CreateView
from django.utils.safestring import mark_safe
import datetime
from django.db.models import Sum,Count

from .utils import Calendar

# Create your views here.
@login_required()
def index(request):
    today = dt.date.today()

    # update all pick ups when user visits home page and when todays date == pick up date
    pick_up_list = PickUpV2.objects.filter(scheduled_user=request.user,scheduled_date__lte=today)
   
    for pick_up in pick_up_list:
        if not pick_up.completed and pick_up.scheduled_date <= today:
            pick_up.completed = True
            pick_up.save()

    # set up notifications for pick ups
        # when pick up is tomorrow
        # when DoS picks up bin
    return render(request,'_base.html')

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
    return datetime.date.today()

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

@login_required()
def dashboard(request):
    context = {}
    pick_up_list = PickUpV2.objects.filter(scheduled_user=request.user,completed=True).order_by('-completed')
    context['bin_type_data'] = pick_up_list.values('bin_type__name','bin_type__id').annotate(total_pounds = Sum('weight'),completed=Count('completed'))
    return render(request,'v2_interface/dashboard.html',context)


class BinPickUpDates(LoginRequiredMixin,ListView):
    template_name = "v2_interface/bin_pickup_dates.html"
    context_object_name = "bin_dates"

    def get_queryset(self,**kwargs):
        print(kwargs)
        return PickUpV2.objects.filter(scheduled_user=self.request.user,bin_type__id=self.kwargs['pk'],completed=True)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        bin_type = WasteBinTypeV2.objects.get(id=self.kwargs['pk'])
        context['bin_name'] = bin_type.name
        return context
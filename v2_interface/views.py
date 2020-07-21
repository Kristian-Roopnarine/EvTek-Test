from django.shortcuts import render
import datetime as dt
from waste_bins.models import PickUp
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.safestring import mark_safe
import datetime

from .utils import Calendar
# Create your views here.
@login_required()
def index(request):
    today = dt.date.today()

    # update all pick ups when user visits home page and when todays date == pick up date
    pick_up_list = PickUp.objects.filter(scheduled_user=request.user,scheduled_date__lte=today)
   
    for pick_up in pick_up_list:
        if not pick_up.completed and pick_up.scheduled_date <= today:
            pick_up.completed = True
            pick_up.save()

    # set up notifications for pick ups
        # when pick up is tomorrow
        # when DoS picks up bin
    return render(request,'_base.html')

class CalendarView(ListView):
    model = PickUp
    template_name = 'v2_interface/calendar.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        # use todays date for the calendar

        d = get_date(self.request.GET.get('day',None))

        # create calendar class
        cal = Calendar(d.year,d.month)

        html_cal = cal.format_month(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year,month = (int(x) for x in req_day.split("-"))
        return date(year,month,day=1)
    return datetime.date.today()
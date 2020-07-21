from datetime import datetime,timedelta,date
from calendar import HTMLCalendar
from .models import PickUpV2

class Calendar(HTMLCalendar):

    def __init__(self,year=None,month=None):
        self.year = year
        self.month = month
        super(Calendar,self).__init__()

    
    # formats a day as a td
    # filters events by day
    def format_day(self,day,pickup):
        pickups = pickup.filter(scheduled_date__day = f'{day}')
        d = ''
        
        for event in pickups:
            url = f'pickup/{event.id}/'
            if event.completed:
                d += f"<li><span class='badge badge-success'><a class='text-white' href={url}>{event.bin_type.name} bin </span></a></li>"
            else:
                d += f'<li><span class="badge badge-warning"><a class="text-dark" href={url}>{event.bin_type.name} bin </span></a></li>'
        
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul style='list-style-type:none;'> {d} </ul></td>" 
        return '<td></td>'

    def format_week(self,theweek,pickup):
        week = ''
        for d,weekday in theweek:
            week += self.format_day(d,pickup)
        return f'<tr> {week} </tr>'
    
    def format_month(self, user, withyear=True):
        pickup_list = PickUpV2.objects.filter(scheduled_user=user)

        cal = f"<table border='0' cellpadding='0' cellspacing='0' class='calendar'>\n"

        cal += f'{self.formatmonthname(self.year,self.month,withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year,self.month):
            cal+=f'{self.format_week(week,pickup_list)}\n'
        cal += '</table>'
        return cal


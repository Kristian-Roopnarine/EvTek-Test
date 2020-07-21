from datetime import datetime,timedelta
from calendar import HTMLCalendar
from waste_bins.models import PickUp

class Calendar(HTMLCalendar):

    def __init__(self,year=None,month=None):
        self.year = year
        self.month = month
        super(Calendar,self).__init__()

    
    # formats a day as a td
    # filters events by day
    def format_day(self,day):
        """
        d = ''
        for event in pickup_per_day:
            d += f'<li>{ event.bin_type__name } </li>'
        """
        if day != 0:
            return f"<td><span class='date'>{day}</span></td>" 
        return '<td></td>'

    def format_week(self,theweek):
        week = ''
        for d,weekday in theweek:
            week += self.format_day(d)
        return f'<tr> {week} </tr>'
    
    def format_month(self,withyear=True):
        cal = f"<table border='0' cellpadding='0' cellspacing='0' class='calendar'>\n"

        cal += f'{self.formatmonthname(self.year,self.month,withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year,self.month):
            cal+=f'{self.formatweek(week)}\n'
        cal += '</table>'
        return cal


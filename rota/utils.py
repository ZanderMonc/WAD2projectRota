from datetime import datetime, timedelta
from calendar import HTMLCalendar
from rota.models import Timetable, Request


class Table(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Table, self).__init__()

    def formatday(self, day,):
        #shifts_on_day = shifts.filter(date_requesting=day)
        d = ''
        #for shift in shifts_on_day:
         #   d += f'<li> {shift}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, week):
        weekstring = ''
        for d, weekday in week:
            weekstring += self.formatday(d)
        return f'<tr> {weekstring} </tr>'

    def formatmonth(self, withyear=True):
        #shifts = Request.objects.all()
        tbl = f'<table border="0" cellpadding="0" cellspacing="0" class="timetable">\n'
        tbl += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        tbl += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            tbl += f'{self.formatweek(week)}\n'
        return tbl

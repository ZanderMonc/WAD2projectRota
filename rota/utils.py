import datetime
from datetime import timedelta
from calendar import HTMLCalendar
from rota.models import Timetable, Request


class Table(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Table, self).__init__()

    def formatday(self, day, shifts):
        shifts_on_day = shifts.filter(request_date__day=day)
        d = ''
        for shift in shifts_on_day:
            d += f'<li> {shift.get_html_url} </li>'
            d += shift.get_shift_time
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, week, shifts):
        shifts = Request.objects.filter(request_date__month=self.month)  # gets this month's shifts
        weekstring = ''
        for d, weekday in week:
            weekstring += self.formatday(d, shifts)
        return f'<tr> {weekstring} </tr>'

    def formatmonth(self, withyear=True):
        shifts = Request.objects.filter(request_date__year=self.year)  # gets only this year's shifts
        tbl = f'<table border="0" cellpadding="0" cellspacing="0" class="timetable">\n'
        tbl += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        tbl += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            tbl += f'{self.formatweek(week, shifts)}\n'
        return tbl

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from rota.models import Timetable, Request


class Table(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Table, self).__init__()

    def dayform(self, day, shifts):
        shifts_on_day = shifts.filter(day=day)
        daystring = ''
        for shift in shifts_on_day:
            daystring += f'<li> {shift.requested_by_staff}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        else:
            return '<td></td>'

    def formatweek(self, week, shifts):
        weekstring = ''
        for day, weekday in week:
            weekstring += self.formatday(day, shifts)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        shifts = Request.objects.getall()
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, shifts)}\n'
        return cal

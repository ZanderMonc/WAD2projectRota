import datetime
from datetime import timedelta
from calendar import HTMLCalendar
from rota.models import Timetable, Request


class Table(HTMLCalendar):#util function creates timetable to be passed as view
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Table, self).__init__()

    def formatday(self, day, shifts):
        shifts_on_day = shifts.filter(request_date__day=day)
        d = ''
        day_list_hcsw = []
        day_list_sn = []
        night_list_hcsw = []
        night_list_sn = []

        for shift in shifts_on_day:
            if shift.get_shift_time == "Day Shift":
                if shift.get_job_title == "Healthcare Support Worker":
                    day_list_hcsw.append(shift)
                else:
                    day_list_sn.append(shift)
            else:
                if shift.get_job_title == "Healthcare Support Worker":
                    night_list_hcsw.append(shift)
                else:
                    night_list_sn.append(shift)

        if (len(day_list_hcsw) or len(day_list_sn)) != 0:
            d += f'<b>Day Shift</b> </br>'
            if len(day_list_sn) != 0:
                d += f'Staff Nurse </br>'
                for shift in day_list_sn:
                    d += f'{shift.get_html_url} </br>'
            if len(day_list_hcsw) != 0:
                d += f'Healthcare Support Worker </br>'
                for shift in day_list_hcsw:
                    d += f'{shift.get_html_url} </br>'
            d += f' </br>'

        if (len(night_list_hcsw) or len(night_list_sn)) != 0:
            d += f'<b>Night Shift</b> </br>'
            if len(night_list_sn) != 0:
                d += f'Staff Nurse </br>'
                for shift in night_list_sn:
                    d += f'{shift.get_html_url} </br>'
            if len(night_list_hcsw) != 0:
                d += f'Healthcare Support Worker </br>'
                for shift in night_list_hcsw:
                    d += f'{shift.get_html_url} </br>'
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


import calendar

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rota.forms import UserForm, UserProfileForm, ShiftForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from .models import *
from .utils import Table

class T(generic.ListView):  # T view represents a timetable
    model = Request
    template_name = 'rota/timetable.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # today's date
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our table class with today's year and date
        r = Table(d.year, d.month)

        # Calling the formatmonth method, which returns our table

        html_rota = r.formatmonth(withyear=True)

        context['timetable'] = mark_safe(html_rota)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

# Return previous month.
def prev_month(d):
    first = d.replace(day=1)
    pr_month = first - timedelta(days=1)
    month = 'month=' + str(pr_month.year) + '-' + str(pr_month.month)
    return month

# Return next month.
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    n_month = last + timedelta(days=1)
    month = 'month=' + str(n_month.year) + '-' + str(n_month.month)
    return month

# Shift view to add a shift
def shift(request, shift_id=None, ):
    instance = Request()
    user = User.objects.get(id=request.user.id)
    userprofile = UserProfile.objects.filter(user=user)[0]
    all_users = User.objects.all()
    if userprofile.job_title == "Charge Nurse":
        if shift_id:
            instance = get_object_or_404(Request, pk=shift_id)
        else:
            instance = Request()

        form = ShiftForm(request.POST or None, instance=instance)
        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('rota:timetable'))
        return render(request, 'rota/shift.html', {'form': form, 'user': user, 'all_users': all_users, })
    return HttpResponseRedirect(reverse('rota:timetable'))

# View to edit a shift
def edit_shift(request, shift_id):
    shift_id = shift_id
    objeto = Request.objects.filter(request_id=shift_id)[0]
    user = User.objects.get(id=request.user.id)
    userprofile = UserProfile.objects.filter(user=user)[0]
    all_users = User.objects.all()
    if userprofile.job_title == "Charge Nurse":
        if shift_id:
            instance = get_object_or_404(Request, pk=shift_id)
        else:
            instance = Request()

        form = ShiftForm(request.POST or None, instance=instance)
        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('rota:timetable'))
        return render(request, 'rota/editshift.html',
                      {'form': form, 'user': user, 'all_users': all_users, "shift_id": shift_id, "objeto":objeto})
    return HttpResponseRedirect(reverse('rota:timetable'))

# View to delete a shift object.
def deleteShift(request, shift_id):
    shift = Request.objects.get(request_id=shift_id)
    shift.delete()
    return redirect('rota:timetable')

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def index(request):
    return render(request, 'rota/index.html', )


def about(request):
    return render(request, 'rota/about.html', )


def contactus(request):
    return render(request, 'rota/contactus.html', )

# Register view to register the user and userprofile models.
def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            return redirect("rota:login")
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "rota/register.html", context={"user_form": user_form,
                                                          "profile_form": profile_form, })

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rota:timetable'))
            else:
                return HttpResponse("Your RotaCare account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rota/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rota:index'))


@login_required
def profile(request):
    return render(request, 'rota/profile.html', )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        update_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if update_form.is_valid:
            update_form.save()
            return redirect('rota:profile')
    else:
        update_form = UpdateProfileForm(instance=request.user)
        args = {
            'form1': update_form,
        }
        return render(request, 'rota/editprofile.html', args)

import calendar

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from rota.forms import UserForm, UserProfileForm, ShiftForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from .models import *
from .utils import Table


# Create your views here.


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


def prev_month(d):
    first = d.replace(day=1)
    pr_month = first - timedelta(days=1)
    month = 'month=' + str(pr_month.year) + '-' + str(pr_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    n_month = last + timedelta(days=1)
    month = 'month=' + str(n_month.year) + '-' + str(n_month.month)
    return month


def shift(request, shift_id=None,):

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
        return render(request, 'rota/shift.html', {'form': form, 'user':user, 'all_users':all_users, })
    return HttpResponseRedirect(reverse('rota:timetable'))



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


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "rota/register.html", context={"user_form": user_form,
                                                          "profile_form": profile_form,
                                                          "registered": registered, })


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rota:timetable'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your RotaCare account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rota/login.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rota:index'))


@login_required
def profile(request):
    return render(request, 'rota/profile.html', )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        update_form = UpdateProfileForm(request.POST, instance=request.user.userprofile)
        if update_form.is_valid:
            update_form.save()
            return redirect('rota:profile')
    else:
        update_form = UpdateProfileForm(instance=request.user)
        args = {
            'form1': update_form,
        }
        return render(request, 'rota/editprofile.html', args)

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.db import transaction

from .models import Movie, Schedule, Reservation
from .forms import LoginForm, ReserveForm, SignUpForm

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import string

def movies_view(request):
    context = {
        'movies': Movie.objects.filter(is_deleted=False),
    }
    return render(request, 'movies.html', context)


def schedule_view(request):
    movie_id = request.GET.get(key="movie_id")
    date_min = datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0)
    date_max = date_min + timedelta(days=14)

    schedules = Schedule.objects.filter(movie=movie_id, start_at__range=[date_min, date_max]).order_by('start_at')

    schedule_array = {}
    start = datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0)
    end = start + timedelta(days=1)
    for _ in range(14):
        date = start.strftime('%Y/%m/%d')
        oneday_schedules = schedules.filter(start_at__range=[start, end]).order_by('start_at')
        schedule_array[date] = oneday_schedules
        start +=  timedelta(days=1)
        end += timedelta(days=1)

    context = {
        'movie': Movie.objects.get(id=movie_id),
        'schedules': schedule_array,
    }
    return render(request, 'schedule.html', context)


def seating_chart_view(request):
    schedule_id = request.GET.get(key="schedule_id")
    reservations = Reservation.objects.filter(schedule=schedule_id, is_deleted=False)

    reservations = [reservation.seat_number for reservation in reservations]

    schedule = Schedule.objects.get(id=schedule_id)
    hole = schedule.hole

    row = {}
    for r in list(string.ascii_uppercase)[:hole.row]:
        col = {}
        for c in range(1, hole.col+1):
            if f'{r}-{c}' in reservations:
                col[c] = 'reserved'
            else:
                col[c] = 'reservable'
            row[r] = col


    context = {
        'seat': row,
        'form': ReserveForm(),
        'schedule': schedule,
        'userform': SignUpForm(),
    }
    return render(request, 'seating_chart.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = addUser(username, password)
            if user == False:
                context = {
                    'errors': 'true',
                    'form': form,
                }
                return render(request, "signup.html", context=context)
        else:
            context = {
                'errors': form.errors,
                'form': form,
            }
            return render(request, "signup.html", context=context)

        login(request, user)
        return HttpResponseRedirect(reverse('movies'))

    else:
        context = {
            'form': SignUpForm(),
        }
        return render(request, "signup.html", context=context)


def signup_and_reservation(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = addUser(username, password)
            if user == False:
                context = {
                    'errors': 'true',
                    'form': form,
                }
                return render(request, "signup.html", context=context)

            login(request, user)

        form = ReserveForm(request.POST)
        if form.is_valid():
            schedule = form.cleaned_data['schedule']
            seat = form.cleaned_data['seat']

            seats = seat.split(',')
            schedule = Schedule.objects.get(id=schedule)
            for seat in seats:
                addReservation(schedule, user, seat)

        return HttpResponseRedirect(reverse('reservation_list'))


def login_view(request):
    # POST
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('movies'))
                else:
                    return HttpResponse("アカウントが有効ではありません")
            else:
                context = {
                    'errors': 'true',
                    'form': form,
                }
                return render(request, 'login.html', context)
        else:
            context = {
                'errors': form.error,
                'form': form,
            }
            return render(request, 'login.html', context)

    # GET
    else:
        form = ReserveForm(request.POST)

        context = {
            'form': LoginForm()
        }
        return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('movies'))


@login_required
def reserve_view(request):
    user = request.user
    form = ReserveForm(request.POST)
    if form.is_valid():
        schedule = form.cleaned_data['schedule']
        seat = form.cleaned_data['seat']

        seats = seat.split(',')
        schedule = Schedule.objects.get(id=schedule)
        for seat in seats:
            addReservation(schedule, user, seat)

    return HttpResponseRedirect(reverse('reservation_list'))


@login_required
def reservation_list_view(request):
    user = request.user
    reservations = getReservationByUser(user)

    toast = request.GET.get(key="toast", default="False")

    context = {
        'reservations': reservations,
        'toast': toast
    }
    return render(request, 'reservation_list.html', context)


@login_required
def delete_reservation_view(request):
    user = request.user
    reservation_id = request.GET.get(key="reservation_id")
    deleteReservationByID(reservation_id)

    return HttpResponseRedirect(reverse('reservation_list'))




def addUser(username, password):
    try:
        with transaction.atomic():
            user = get_user_model().objects.create_user(
                username=username,
                password=password
            )
            return user
    except:
        return False

def addReservation(schedule, user, seat):
    try:
        with transaction.atomic():
            r = Reservation(schedule=schedule, user=user, seat_number=seat)
            r.save()
            return True
    except:
        return False

def deleteReservationByID(id):
    try:
        with transaction.atomic():
            reservation = Reservation.objects.get(id=id)
            reservation.is_deleted = True
            reservation.save()
            return True
    except:
        return False

def getReservationByID(id):
    reservation = Reservation.objects.get(id=id)

    return reservation

def getReservationByUser(user):
    reservations = Reservation.objects.filter(user=user, is_deleted=False).order_by('schedule')

    return reservations
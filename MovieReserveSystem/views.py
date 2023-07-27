from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import TemplateView #テンプレートタグ
from .forms import LoginForm, ReserveForm, SignUpForm

# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Movie, Schedule, Reservation


from datetime import datetime
from datetime import timedelta
from datetime import timezone


from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from django.db import transaction

from django.contrib.auth import get_user_model
import string


# Create your views here.

def movies(request):
    context = {
        'movies': Movie.objects.all(),
    }
    return render(request, 'movies.html', context)


def addUser(username, email, password):
    user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )
    login(request, user)
    return user

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = get_user_model().objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password']
                    )
                    login(request, user)
                    return HttpResponseRedirect(reverse('movies'))
            except:
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

    else:
        context = {
            'form': SignUpForm(),
        }
        return render(request, "signup.html", context=context)



def signup_and_reservation(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = get_user_model().objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password']
                    )
                    login(request, user)
            except:
                context = {
                    'errors': 'true',
                    'form': form,
                }
                return render(request, "signup.html", context=context)

        form = ReserveForm(request.POST)
        if form.is_valid():
            schedule = form.cleaned_data['schedule']
            seat = form.cleaned_data['seat']
            seats = seat.split(',')


            for seat in seats:
                s = Schedule.objects.get(id=schedule)
                r = Reservation(schedule=s, user=user, seat_number=seat)
                r.save()

        return HttpResponseRedirect(reverse('reservation_list'))




def login_view(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Djangoの認証機能
            user = authenticate(username=username, password=password)

            # ユーザー認証
            if user:
                #ユーザーアクティベート判定
                if user.is_active:
                    # ログイン
                    login(request,user)
                    # ホームページ遷移
                    return HttpResponseRedirect(reverse('movies'))
                else:
                    # アカウント利用不可
                    return HttpResponse("アカウントが有効ではありません")
            # ユーザー認証失敗
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
        if form.is_valid():
            schedule = form.cleaned_data['schedule']
            seat = form.cleaned_data['seat']

        context = {
            'form': LoginForm()
        }
        return render(request, 'login.html', context)

@login_required
def logout_view(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('movies'))


def datas(request):

    movie_id = request.GET.get(key="movie_id", default="8b1168d1-52fa-456d-b936-53e60a9b8ae6")
    date_min = datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0)
    date_max = date_min + timedelta(days=14)
    schedules = Schedule.objects.filter(movie=movie_id, start_at__range=[date_min, date_max]).order_by('start_at')

    schedule_array = {}
    start = datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0)
    end = start + timedelta(days=1)
    for _ in range(14):
        # tstr = start.strftime('%Y/%m/%d (%A)')
        tstr = start.strftime('%Y/%m/%d')
        oneday_schedules = schedules.filter(start_at__range=[start, end]).order_by('start_at')
        schedule_array[tstr] = oneday_schedules
        start +=  timedelta(days=1)
        end += timedelta(days=1)

    context = {
        'movie': Movie.objects.get(id=movie_id),
        'schedules': schedule_array,
    }
    return render(request, 'datas.html', context)


def seating_chart_view(request):
    schedule_id = request.GET.get(key="schedule_id", default="8b1168d1-52fa-456d-b936-53e60a9b8ae6")
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
        'schedule': Schedule.objects.get(id=schedule_id),
        'userform': SignUpForm(),
    }
    return render(request, 'seating_chart.html', context)


# def add_reservation(s, u, seat):
#     s = Schedule.objects.get(id=schedule)
#     r = Reservation(schedule=s, user=user, seat_number=seat)
#     r.save()


def reserve_view(request):
    user = request.user
    form = ReserveForm(request.POST)
    if form.is_valid():
        schedule = form.cleaned_data['schedule']
        seat = form.cleaned_data['seat']
        seats = seat.split(',')

        for seat in seats:
            s = Schedule.objects.get(id=schedule)
            r = Reservation(schedule=s, user=user, seat_number=seat)
            r.save()

    return HttpResponseRedirect(reverse('reservation_list'))


@login_required
def reservation_list_view(request):
    user = request.user

    reservations = Reservation.objects.filter(user=user, is_deleted=False).order_by('schedule')
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
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.is_deleted = True
    reservation.save()

    return HttpResponseRedirect(reverse('reservation_list'))
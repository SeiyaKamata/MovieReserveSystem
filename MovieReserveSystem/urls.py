from . import views
from django.urls import path

urlpatterns = [
    path('', views.movies),
    path('signup/', views.signup_view, name='signup'),
    path('signup_and_reservation/', views.signup_and_reservation, name='signup_and_reservation'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('movies/', views.movies, name='movies'),
    path('datas/', views.datas, name='datas'),
    path('seating_chart/', views.seating_chart_view, name='seating_chart'),
    path('reserve_view/', views.reserve_view, name='reserve_view'),
    path('reservation_list/', views.reservation_list_view, name='reservation_list'),
]
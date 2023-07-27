from . import views
from django.urls import path

urlpatterns = [
    path('', views.movies_view),
    path('addseat/', views.add_seat_view, name='addseat'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('movies/', views.movies_view, name='movies'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('seating_chart/', views.seating_chart_view, name='seating_chart'),
    path('reserve/', views.reserve_view, name='reserve'),
    path('reservation_list/', views.reservation_list_view, name='reservation_list'),
    path('delete_reservation/', views.delete_reservation_view, name='delete_reservation'),
    path('signup_and_reservation/', views.signup_and_reservation, name='signup_and_reservation'),
]
# parents/urls.py
from django.urls import path
from . import views

app_name = 'parents'

urlpatterns = [
    path('', views.parent_dashboard, name='dashboard'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('check-in-out/', views.check_in_out_list, name='check_in_out_list'),
    path('fees/', views.fee_list, name='fee_list'),
    path('notifications/', views.notification_list, name='notification_list'),

    path('change/password/', views.change_password, name='change_password'),
]
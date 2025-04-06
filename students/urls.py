from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_dashboard, name='dashboard'),
    path('food-preferences/', views.food_preference_list, name='food_preference_list'),
    path('food-menu/', views.food_menu_list, name='food_menu_list'),
    path('food-preferences/add/', views.food_preference_add, name='food_preference_add'),
    path('wash-slots/', views.wash_slot_list, name='wash_slot_list'),
    path('wash-slots/book/<int:slot_id>/', views.wash_slot_book, name='wash_slot_book'),
    path('wash-slots/complete/<int:slot_id>/', views.wash_slot_complete, name='wash_slot_complete'),
    path('fees/', views.fee_list, name='fee_list'),
    path('mess-cuts/', views.mess_cut_list, name='mess_cut_list'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/add/', views.complaint_add, name='complaint_add'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('check-in-out/', views.check_in_out_list, name='check_in_out_list'),
    path('check-in/add/', views.check_in_add, name='check_in_add'),
    path('check-out/add/', views.check_out_add, name='check_out_add'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('change/password/', views.change_password, name='change_password'),

]
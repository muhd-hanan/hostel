# faculty/urls.py
from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    path('', views.faculty_dashboard, name='dashboard'),

    
    
    path('food-menu/', views.food_menu_list, name='food_menu_list'),
    path('food-menu/count/', views.food_count_list, name='food_count_list'),
    path('food-menu/add/', views.food_menu_add, name='food_menu_add'),
    path('food-menu/<int:pk>/update/', views.food_menu_update, name='food_menu_update'),

    path('mess-cuts/', views.mess_cut_list, name='mess_cut_list'),
    path('mess-cuts/update/<int:id>/', views.mess_cut_update, name='mess_cut_update'),
    
    path('wash-slots/', views.wash_slot_list, name='wash_slot_list'),
    path('wash-slots/add/', views.wash_slot_add, name='wash_slot_add'),
    path('wash-slots/<int:pk>/update/', views.wash_slot_update, name='wash_slot_update'),
    
    path('fees/', views.fee_list, name='fee_list'),
    path('fees/add/', views.fee_add, name='fee_add'),
    path('fees/<int:pk>/update/', views.fee_update, name='fee_update'),
    
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/<int:pk>/update/', views.complaint_update, name='complaint_update'),
    
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
    
    path('check-in-out/', views.check_in_out_list, name='check_in_out_list'),
    path('check-in-out/<int:pk>/approve/', views.check_in_out_approve, name='check_in_out_approve'),
    
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/add/', views.notification_add, name='notification_add'),
    
    path('parent-student/', views.parent_student_list, name='parent_student_list'),
    path('parent-student/add/', views.parent_student_add, name='parent_student_add'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('parents/', views.parent_list, name='parent_list'),
    path('parents/add/', views.parent_add, name='parent_add'),

    path('change/password/', views.change_password, name='change_password'),

]


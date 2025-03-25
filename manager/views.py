from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from faculty.models import FoodMenu, WashSlot
from students.models import Fee, Complaint, Attendance, CheckInOut, Notification, FoodPreference
from parents.models import ParentStudent
from django.contrib.auth import authenticate, login, logout
from users.models import User
from faculty.forms import (
    FoodMenuForm, WashSlotForm, FeeForm, ComplaintForm, AttendanceForm,
    CheckInOutForm, NotificationForm, ParentStudentForm, StudentCreateForm, ParentCreateForm, FeeAddForm, FacultyCreateForm
)
from django.db.models import Count
from datetime import date

from django.utils import timezone

# Decorator to check if user is faculty
def manager_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func

# Dashboard
@manager_required
def manager_dashboard(request):
    return render(request, 'manager/dashboard.html')

# Food Menu Views
@manager_required
def food_menu_list(request):
    food_menus = FoodMenu.objects.all()
    return render(request, 'manager/food_menu_list.html', {'food_menus': food_menus})


@manager_required
def food_count_list(request):
    today = timezone.now().date()

    breakfast = FoodPreference.objects.filter(
        date=today, breakfast=True
    ).count()
    lunch = FoodPreference.objects.filter(
        date=today, lunch=True
    ).count()
    snack = FoodPreference.objects.filter(
        date=today, snack=True
    ).count()
    dinner = FoodPreference.objects.filter(
        date=today, dinner=True
    ).count()

    return render(request, 'manager/food_count.html', {
        'breakfast': breakfast,
        'lunch': lunch,
        'snack': snack,
        'dinner': dinner,
    })



@manager_required
def food_menu_add(request):
    if request.method == 'POST':
        form = FoodMenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_by = request.user
            menu.updated_by = request.user
            menu.save()
            messages.success(request, "Food menu added successfully.")
            return redirect('manager:food_menu_list')
    else:
        form = FoodMenuForm()
    return render(request, 'manager/food_menu_form.html', {'form': form})

@manager_required
def food_menu_update(request, pk):
    menu = get_object_or_404(FoodMenu, pk=pk)
    if request.method == 'POST':
        form = FoodMenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.updated_by = request.user
            menu.save()
            messages.success(request, "Food menu updated successfully.")
            return redirect('manager:food_menu_list')
    else:
        form = FoodMenuForm(instance=menu)
    return render(request, 'manager/food_menu_form.html', {'form': form})

@manager_required
def wash_slot_list(request):
    wash_slots = WashSlot.objects.annotate(student_count=Count('students')).all()
    return render(request, 'manager/wash_slot_list.html', {'wash_slots': wash_slots})

@manager_required
def wash_slot_add(request):
    if request.method == 'POST':
        form = WashSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.created_by = request.user
            slot.updated_by = request.user
            slot.save()
            messages.success(request, "Wash slot added successfully.")
            return redirect('manager:wash_slot_list')
    else:
        form = WashSlotForm()
    return render(request, 'manager/wash_slot_form.html', {'form': form})

@manager_required
def wash_slot_update(request, pk):
    slot = get_object_or_404(WashSlot, pk=pk)
    if request.method == 'POST':
        form = WashSlotForm(request.POST, instance=slot)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.updated_by = request.user
            slot.save()
            messages.success(request, "Wash slot updated successfully.")
            return redirect('manager:wash_slot_list')
    else:
        form = WashSlotForm(instance=slot)
    return render(request, 'manager/wash_slot_form.html', {'form': form})

@manager_required
def fee_list(request):
    fees = Fee.objects.all()
    return render(request, 'manager/fee_list.html', {'fees': fees})


@manager_required
def fee_add(request):
    if request.method == 'POST':
        form = FeeAddForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.updated_by = request.user
            fee.save()
            messages.success(request, "Fee status updated successfully.")
            return redirect('manager:fee_list')
    else:
        form = FeeAddForm()
    return render(request, 'manager/fee_form.html', {'form': form})


@manager_required
def fee_update(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.updated_by = request.user
            fee.save()
            messages.success(request, "Fee status updated successfully.")
            return redirect('manager:fee_list')
    else:
        form = FeeForm(instance=fee)
    return render(request, 'manager/fee_form.html', {'form': form, 'fee': fee})

@manager_required
def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'manager/complaint_list.html', {'complaints': complaints})

@manager_required
def complaint_update(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            if complaint.status == 'resolved':
                complaint.resolved_by = request.user
            complaint.updated_by = request.user
            complaint.save()
            messages.success(request, "Complaint updated successfully.")
            return redirect('manager:complaint_list')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'manager/complaint_form.html', {'form': form, 'complaint': complaint})

@manager_required
def attendance_list(request):
    selected_date = request.GET.get('date')
    attendance_records = Attendance.objects.all()
    
    if selected_date:
        attendance_records = attendance_records.filter(date=selected_date)
        
    return render(request, 'manager/attendance_list.html', {
        'attendance_records': attendance_records,
        'selected_date': selected_date
    })

@manager_required
def attendance_mark(request):
    students = User.objects.filter(is_student=True)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            # Process attendance for all students
            for student in students:
                is_present = request.POST.get(f'present_{student.id}') == 'on'
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={'is_present': is_present}
                )
            messages.success(request, "Attendance marked successfully for all students.")
            return redirect('manager:attendance_list') 
    else:
        form = AttendanceForm(initial={'date': date.today()})
    
    selected_date = form.initial['date'] if not request.POST else request.POST.get('date')
    attendance_records = Attendance.objects.filter(date=selected_date).select_related('student')
    attendance_dict = {record.student.id: record.is_present for record in attendance_records}
    
    return render(request, 'manager/attendance_form.html', {
        'form': form,
        'students': students,
        'attendance_dict': attendance_dict,
        'selected_date': selected_date
    })

@manager_required
def check_in_out_list(request):
    check_ins = CheckInOut.objects.all()
    return render(request, 'manager/check_in_out_list.html', {'check_ins': check_ins})

@manager_required
def check_in_out_approve(request, pk):
    check_in_out = get_object_or_404(CheckInOut, pk=pk)
    if request.method == 'POST':
        form = CheckInOutForm(request.POST, instance=check_in_out)
        if form.is_valid():
            check_in_out = form.save(commit=False)
            check_in_out.approved_by = request.user
            check_in_out.updated_by = request.user
            check_in_out.save()
            messages.success(request, "Check in/out approved successfully.")
            return redirect('manager:check_in_out_list')
    else:
        form = CheckInOutForm(instance=check_in_out)
    return render(request, 'manager/check_in_out_form.html', {'form': form, 'check_in_out': check_in_out})

@manager_required
def notification_list(request):
    notifications = Notification.objects.filter(sender=request.user)
    return render(request, 'manager/notification_list.html', {'notifications': notifications})

@manager_required
def notification_add(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.sender = request.user
            notification.created_by = request.user
            notification.updated_by = request.user
            notification.save()
            messages.success(request, "Notification sent successfully.")
            return redirect('manager:notification_list')
    else:
        form = NotificationForm()
    return render(request, 'manager/notification_form.html', {'form': form})

@manager_required
def parent_student_list(request):
    relationships = ParentStudent.objects.all()
    return render(request, 'manager/parent_student_list.html', {'relationships': relationships})

@manager_required
def parent_student_add(request):
    if request.method == 'POST':
        form = ParentStudentForm(request.POST)
        if form.is_valid():
            relationship = form.save(commit=False)
            relationship.created_by = request.user
            relationship.updated_by = request.user
            relationship.save()
            messages.success(request, "Parent-student relationship added successfully.")
            return redirect('manager:parent_student_list')
    else:
        form = ParentStudentForm()
    return render(request, 'manager/parent_student_form.html', {'form': form})

@manager_required
def student_list(request):
    students = User.objects.filter(is_student=True)
    return render(request, 'manager/student_list.html', {'students': students})

@manager_required
def student_add(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student {student.email} created successfully.")
            return redirect('manager:student_list')
    else:
        form = StudentCreateForm()
    return render(request, 'manager/student_form.html', {'form': form})

@manager_required
def parent_list(request):
    parents = User.objects.filter(is_parent=True)
    return render(request, 'manager/parent_list.html', {'parents': parents})

@manager_required
def parent_add(request):
    if request.method == 'POST':
        form = ParentCreateForm(request.POST)
        if form.is_valid():
            parent = form.save()
            messages.success(request, f"Parent {parent.email} created successfully.")
            return redirect('manager:parent_list')
    else:
        form = ParentCreateForm()
    return render(request, 'manager/parent_form.html', {'form': form})


@manager_required
def faculty_list(request):
    faculty = User.objects.filter(is_faculty=True)
    return render(request, 'manager/faculty_list.html', {'faculty': faculty})

@manager_required
def faculty_add(request):
    if request.method == 'POST':
        form = FacultyCreateForm(request.POST)
        if form.is_valid():
            faculty = form.save()
            messages.success(request, f"faculty {faculty.email} created successfully.")
            return redirect('manager:faculty_list')
    else:
        form = FacultyCreateForm()
    return render(request, 'manager/faculty_form.html', {'form': form})


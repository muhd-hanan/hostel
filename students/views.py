# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import FoodPreference, WashBooking, Fee, Complaint, Attendance, CheckInOut, Notification, MessCut
from faculty.models import WashSlot, FoodMenu
from .forms import FoodPreferenceForm, WashBookingForm, ComplaintForm, CheckInForm, CheckOutForm
from faculty.forms import PasswordChangeForm
from django.db.models import Count
from datetime import timedelta, date
from django.contrib.auth import update_session_auth_hash


def student_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_student)(view_func))
    return decorated_view_func

@student_required
def student_dashboard(request):
    return render(request, 'students/dashboard.html')

@student_required
def food_menu_list(request):
    food_menus = FoodMenu.objects.all()
    return render(request, 'students/food_menu_list.html', {'food_menus': food_menus})

@student_required
def food_preference_list(request):
    preferences = FoodPreference.objects.filter(student=request.user)
    return render(request, 'students/food_preference_list.html', {'preferences': preferences})

@student_required
def food_preference_add(request):
    if request.method == 'POST':
        form = FoodPreferenceForm(request.POST)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.student = request.user
            preference.created_by = request.user
            preference.updated_by = request.user
            preference.save()
            messages.success(request, "Food preference added successfully.")
            return redirect('students:food_preference_list')
    else:
        form = FoodPreferenceForm()
    return render(request, 'students/food_preference_form.html', {'form': form})

@student_required
def wash_slot_list(request):
    student=request.user
    wash_slots = WashSlot.objects.annotate(student_count=Count('students')).all()
    return render(request, 'students/wash_slot_list.html', {'wash_slots': wash_slots, 'student':student})

@student_required
def wash_slot_book(request, slot_id):
    student = request.user
    slot = get_object_or_404(WashSlot, id=slot_id)
    if slot.students.count() >= slot.max_capacity:
        messages.error(request, "This wash slot is already full.")
    elif student in slot.students.all():
        messages.info(request, "You have already booked this slot.")
    else:
        slot.students.add(student)
        slot.save()
        messages.success(request, "Wash slot booked successfully.")
    return redirect('students:wash_slot_list')

@student_required
def wash_slot_complete(request, slot_id):
    student = request.user
    slot = get_object_or_404(WashSlot, id=slot_id)
    if student in slot.students.all():
        slot.students.remove(student)
        slot.save()
        messages.success(request, "Washing completed successfully.")
    else:
        messages.error(request, "You are not booked for this slot.")
    return redirect('students:wash_slot_list')

@student_required
def fee_list(request):
    fees = Fee.objects.filter(student=request.user)
    return render(request, 'students/fee_list.html', {'fees': fees})

@student_required
def mess_cut_list(request):
    # Get current user (student)
    student = request.user
    
    # Get the last 6 days of attendance records
    attendance_records = Attendance.objects.filter(
        student=student,
        date__gte=date.today() - timedelta(days=6)
    ).order_by('-date')[:6]
    
    # Get existing mess cuts
    cuts = MessCut.objects.filter(student=student)
    
    # Check if student was absent for last 6 days
    if len(attendance_records) == 6:  # Ensure we have 6 days of records
        all_absent = all(not record.is_present for record in attendance_records)
        
        if all_absent:
            # Calculate dates for the mess cut
            end_date = date.today()
            start_date = end_date - timedelta(days=5)  # 6 days total including start and end
            
            # Check if a mess cut already exists for these dates
            existing_cut = MessCut.objects.filter(
                student=student,
                start_date=start_date,
                end_date=end_date
            ).exists()
            
            if not existing_cut:
                # Create new mess cut
                MessCut.objects.create(
                    student=student,
                    start_date=start_date,
                    end_date=end_date,
                    is_paid=False
                )
                # Refresh cuts after creation
                cuts = MessCut.objects.filter(student=student)

    # Pass both cuts and attendance to template for display if needed
    context = {
        'cuts': cuts,
        'attendance': attendance_records,
    }
    return render(request, 'students/cut_list.html', context)

@student_required
def complaint_list(request):
    complaints = Complaint.objects.filter(student=request.user)
    return render(request, 'students/complaint_list.html', {'complaints': complaints})

@student_required
def complaint_add(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.created_by = request.user
            complaint.updated_by = request.user
            complaint.save()
            messages.success(request, "Complaint submitted successfully.")
            return redirect('students:complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'students/complaint_form.html', {'form': form})

@student_required
def attendance_list(request):
    attendance_records = Attendance.objects.filter(student=request.user)
    return render(request, 'students/attendance_list.html', {'attendance_records': attendance_records})

@student_required
def check_in_out_list(request):
    check_ins = CheckInOut.objects.filter(student=request.user)
    return render(request, 'students/check_in_out_list.html', {'check_ins': check_ins})

# @student_required
# def check_in_add(request):
#     if request.method == 'POST':
#         form = CheckInForm(request.POST)
#         if form.is_valid():
#             check_in_datetime = form.cleaned_data['check_in']
#             existing_record = CheckInOut.objects.filter(
#                 student=request.user,
#                 check_in__date=check_in_datetime.date()
#             ).exists()
#             if existing_record:
#                 messages.error(request, "A check-in already exists for this date.")
#                 return render(request, 'students/check_in_out_form.html', {'form': form})
            
#             existing_record = CheckInOut.objects.filter(
#                 student=request.user,
#                 check_out__date=check_in_datetime.date()
#             ).exists()
#             if existing_record:
#                 checkout = CheckInOut.objects.get(student=request.user, check_out__date=check_in_datetime.date())
#                 checkout.check_out = check_in_datetime
#                 checkout.save()
#                 messages.success(request, "Check in/out request submitted successfully.")
#                 return redirect('students:check_in_out_list')
#             check_in_out = form.save(commit=False)
#             check_in_out.student = request.user
#             check_in_out.created_by = request.user
#             check_in_out.updated_by = request.user
#             check_in_out.save()
#             messages.success(request, "Check in/out request submitted successfully.")
#             return redirect('students:check_in_out_list')
#     else:
#         form = CheckInForm()
#     return render(request, 'students/check_in_out_form.html', {'form': form})


@student_required
def check_in_add(request):
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            check_in_out = form.save(commit=False)
            check_in_out.student = request.user
            check_in_out.created_by = request.user
            check_in_out.updated_by = request.user
            check_in_out.save()
            messages.success(request, "Check in/out request submitted successfully.")
            return redirect('students:check_in_out_list')
    else:
        form = CheckInForm()
    return render(request, 'students/check_in_out_form.html', {'form': form})


@student_required
def check_out_add(request):
    last_check_in = CheckInOut.objects.filter(check_out=None).first()
    if last_check_in is None:
        messages.error(request, "No previous check-in found.")
        return redirect('students:check_in_out_list')
    if request.method == 'POST':
        form = CheckOutForm(request.POST, instance=last_check_in)
        if form.is_valid():
            check_in_out = form.save(commit=False)
            check_in_out.save()
            messages.success(request, "Check in/out request submitted successfully.")
            return redirect('students:check_in_out_list')
    else:
        form = CheckOutForm(instance=last_check_in)
    return render(request, 'students/check_in_out_form.html', {'form': form})

@student_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient="Students")
    return render(request, 'students/notification_list.html', {'notifications': notifications})

@student_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('parents:dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'parents/change_password.html', {'form': form})
# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import FoodPreference, WashBooking, Fee, Complaint, Attendance, CheckInOut, Notification
from faculty.models import WashSlot
from .forms import FoodPreferenceForm, WashBookingForm, ComplaintForm, CheckInOutForm

def student_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_student)(view_func))
    return decorated_view_func

@student_required
def student_dashboard(request):
    return render(request, 'students/dashboard.html')

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
    all_slots = WashSlot.objects.all()
    bookings = WashBooking.objects.filter(student=request.user)
    booked_slot_ids = bookings.values_list('slot_id', flat=True)
    available_slots = all_slots.exclude(id__in=booked_slot_ids)
    return render(request, 'students/wash_slot_list.html', {'available_slots': available_slots, 'bookings': bookings})

@student_required
def wash_slot_book(request, slot_id):
    slot = get_object_or_404(WashSlot, id=slot_id)
    if request.method == 'POST':
        form = WashBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            booking.created_by = request.user
            booking.updated_by = request.user
            booking.save()
            messages.success(request, "Wash slot booked successfully.")
            return redirect('students:wash_slot_list')
    else:
        form = WashBookingForm(initial={'slot': slot})
    return render(request, 'students/wash_slot_book.html', {'form': form, 'slot': slot})

@student_required
def fee_list(request):
    fees = Fee.objects.filter(student=request.user)
    return render(request, 'students/fee_list.html', {'fees': fees})

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

@student_required
def check_in_out_add(request):
    if request.method == 'POST':
        form = CheckInOutForm(request.POST)
        if form.is_valid():
            check_in_out = form.save(commit=False)
            check_in_out.student = request.user
            check_in_out.created_by = request.user
            check_in_out.updated_by = request.user
            check_in_out.save()
            messages.success(request, "Check in/out request submitted successfully.")
            return redirect('students:check_in_out_list')
    else:
        form = CheckInOutForm()
    return render(request, 'students/check_in_out_form.html', {'form': form})

@student_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'students/notification_list.html', {'notifications': notifications})
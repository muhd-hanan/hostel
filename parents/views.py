# parents/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from students.models import Attendance, CheckInOut, Fee, Notification
from parents.models import ParentStudent
from faculty.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def parent_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_parent)(view_func))
    return decorated_view_func

@parent_required
def parent_dashboard(request):
    return render(request, 'parents/dashboard.html')

@parent_required
def attendance_list(request):
    # Get students linked to this parent
    relationships = ParentStudent.objects.filter(parent=request.user)
    student_ids = relationships.values_list('student_id', flat=True)
    attendance_records = Attendance.objects.filter(student__id__in=student_ids)
    return render(request, 'parents/attendance_list.html', {'attendance_records': attendance_records})

@parent_required
def check_in_out_list(request):
    relationships = ParentStudent.objects.filter(parent=request.user)
    student_ids = relationships.values_list('student_id', flat=True)
    check_ins = CheckInOut.objects.filter(student__id__in=student_ids)
    return render(request, 'parents/check_in_out_list.html', {'check_ins': check_ins})

@parent_required
def fee_list(request):
    relationships = ParentStudent.objects.filter(parent=request.user)
    student_ids = relationships.values_list('student_id', flat=True)
    fees = Fee.objects.filter(student__id__in=student_ids)
    return render(request, 'parents/fee_list.html', {'fees': fees})

@parent_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient="Parents")
    return render(request, 'parents/notification_list.html', {'notifications': notifications})


@parent_required
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
from django.db import models
from common.models import CommonModel
from users.models import User
from faculty.models import FoodMenu, WashSlot

from django.db import models
from common.models import CommonModel
from users.models import User
from faculty.models import FoodMenu, WashSlot

NOTIFICATION_CHOICES = (
    ('Students', 'Students'),
    ('Parents', 'Parents'),
)

class FoodPreference(CommonModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_preferences')
    date = models.DateField()
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    snack = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)

    class Meta:
        db_table = 'students_foodpreference'
        verbose_name = 'food preference'
        verbose_name_plural = 'food preferences'
        ordering = ["-date"]
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date}"

class WashBooking(CommonModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wash_bookings')
    slot = models.ForeignKey(WashSlot, on_delete=models.CASCADE, related_name='bookings')

    class Meta:
        db_table = 'students_washbooking'
        verbose_name = 'wash booking'
        verbose_name_plural = 'wash bookings'
        ordering = ["-id"]
        unique_together = ('student', 'slot')

class Fee(CommonModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fees', limit_choices_to={'is_student':True})
    amount = models.FloatField()
    due_date = models.DateField()
    paid_amount = models.FloatField(default=0)
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, 
                            choices=(('pending', 'Pending'), 
                                   ('partial', 'Partial'),
                                   ('paid', 'Paid')),
                            default='pending')

    class Meta:
        db_table = 'students_fee'
        verbose_name = 'fee'
        verbose_name_plural = 'fees'
        ordering = ["-due_date"]

class Complaint(CommonModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    description = models.TextField()
    status = models.CharField(max_length=20, 
                            choices=(('pending', 'Pending'),
                                   ('in_progress', 'In Progress'),
                                   ('resolved', 'Resolved')),
                            default='pending')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='resolved_complaints')

    class Meta:
        db_table = 'students_complaint'
        verbose_name = 'complaint'
        verbose_name_plural = 'complaints'
        ordering = ["-created_datetime"]

class Attendance(CommonModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        db_table = 'students_attendance'
        verbose_name = 'attendance'
        verbose_name_plural = 'attendances'
        ordering = ["-date"]
        unique_together = ('student', 'date')


class MessCut(CommonModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messcut_records')
    start_date = models.DateField()
    end_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'students_mess_cut'
        verbose_name = 'mess_cut'
        verbose_name_plural = 'mess_cuts'
        ordering = ["-start_date"]
        

class CheckInOut(CommonModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='check_ins')
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='approved_check_ins')  # Added unique related_name

    class Meta:
        db_table = 'students_checkinout'
        verbose_name = 'check in/out'
        verbose_name_plural = 'check ins/outs'
        ordering = ["-check_in"]


class Notification(CommonModel):
    recipient = models.CharField(max_length=25, choices=NOTIFICATION_CHOICES, default="Parent")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                             related_name='sent_notifications')

    class Meta:
        db_table = 'students_notification'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ["-created_datetime"]
# students/forms.py
from django import forms
from .models import FoodPreference, WashBooking, Complaint, CheckInOut, Notification
from faculty.models import WashSlot

class FoodPreferenceForm(forms.ModelForm):
    class Meta:
        model = FoodPreference
        fields = ['date', 'breakfast', 'lunch', 'snack', 'dinner']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class WashBookingForm(forms.ModelForm):
    class Meta:
        model = WashBooking
        fields = ['slot']
        widgets = {
            'slot': forms.HiddenInput(),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckInOut
        fields = ['check_in']
        widgets = {
            'check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckInOut
        fields = ['check_in','check_out']
        widgets = {
            'check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'check_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
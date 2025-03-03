# faculty/forms.py
from django import forms
from .models import FoodMenu, WashSlot
from students.models import Fee, Complaint, Attendance, CheckInOut, Notification
from parents.models import ParentStudent
from users.models import User

class FoodMenuForm(forms.ModelForm):
    class Meta:
        model = FoodMenu
        fields = ['date', 'meal_type', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class WashSlotForm(forms.ModelForm):
    class Meta:
        model = WashSlot
        fields = ['date', 'start_time', 'end_time', 'max_capacity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['paid_amount', 'paid_date', 'status']
        widgets = {
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']

class AttendanceForm(forms.Form):
    student = forms.ModelChoiceField(queryset=User.objects.filter(is_student=True))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    is_present = forms.BooleanField(required=False)

class CheckInOutForm(forms.ModelForm):
    class Meta:
        model = CheckInOut
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'check_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class NotificationForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
    
    class Meta:
        model = Notification
        fields = ['recipient', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class ParentStudentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=User.objects.filter(is_parent=True))
    student = forms.ModelChoiceField(queryset=User.objects.filter(is_student=True))
    
    class Meta:
        model = ParentStudent
        fields = ['parent', 'student', 'relationship']



class StudentCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ParentCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_parent = True
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
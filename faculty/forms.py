# faculty/forms.py
from django import forms
from .models import FoodMenu, WashSlot
from students.models import Fee, Complaint, Attendance, CheckInOut, Notification
from parents.models import ParentStudent
from users.models import User

class FoodMenuForm(forms.ModelForm):
    class Meta:
        model = FoodMenu
        fields = ['day', 'breakfast', 'lunch', 'snack', 'dinner']

class WashSlotForm(forms.ModelForm):
    class Meta:
        model = WashSlot
        fields = ['start_time', 'end_time', 'max_capacity']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class FeeAddForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['amount', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
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
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Select Date"
    )

class CheckInOutForm(forms.ModelForm):
    class Meta:
        model = CheckInOut
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'check_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class NotificationForm(forms.ModelForm):
    
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
    


class FacultyCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_faculty = True
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password
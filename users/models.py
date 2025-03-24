from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True, 
                            error_messages={'unique': "Email already used"})
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    is_student = models.BooleanField('Is student', default=False)
    is_faculty = models.BooleanField('Is faculty', default=False)
    is_parent = models.BooleanField('Is parent', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    class Meta:
        db_table = 'user_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ["-id"]

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
    


class OTP(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    created_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_otp'
        verbose_name = 'otp'
        verbose_name_plural = 'otps'
        ordering = ["-id"]

    def __str__(self):

        return f'{self.user.email}--{self.otp}'
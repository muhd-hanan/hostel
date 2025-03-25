from django.db import models
from common.models import CommonModel
from users.models import User

class FoodMenu(CommonModel):
    DAY_CHOICES = (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
    
    day = models.CharField(max_length=9, choices=DAY_CHOICES, default='sunday')  # Longest day name is "Wednesday" (9 chars)
    breakfast = models.CharField(max_length=256, null=True, blank=True)
    lunch = models.CharField(max_length=256, null=True, blank=True)
    snack = models.CharField(max_length=256, null=True, blank=True)
    dinner = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'faculty_foodmenu'
        verbose_name = 'food menu'
        verbose_name_plural = 'food menus'
        ordering = ["-id"]  # Note: Changed "-date" to "day" since it's not a DateField

    def __str__(self):
        return f"{self.day}"

class WashSlot(CommonModel):
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_capacity = models.PositiveIntegerField(default=10)
    students = models.ManyToManyField(User, limit_choices_to={'is_student':True}, related_name="whash_slot")

    class Meta:
        db_table = 'faculty_washslot'
        verbose_name = 'wash slot'
        verbose_name_plural = 'wash slots'
        ordering = ["start_time"]

    def __str__(self):
        return f'{self.start_time}-{self.end_time}'
from django.db import models
from common.models import CommonModel
from users.models import User

class FoodMenu(CommonModel):
    MEAL_TYPES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snack', 'Evening Snack'),
        ('dinner', 'Dinner'),
    )
    
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    description = models.TextField()

    class Meta:
        db_table = 'faculty_foodmenu'
        verbose_name = 'food menu'
        verbose_name_plural = 'food menus'
        ordering = ["-date", "meal_type"]
        unique_together = ('date', 'meal_type')

    def __str__(self):
        return f"{self.date} - {self.meal_type}"

class WashSlot(CommonModel):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_capacity = models.PositiveIntegerField(default=10)

    class Meta:
        db_table = 'faculty_washslot'
        verbose_name = 'wash slot'
        verbose_name_plural = 'wash slots'
        ordering = ["-date", "start_time"]

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time}"
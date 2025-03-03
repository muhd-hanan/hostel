# parents/models.py
from django.db import models
from common.models import CommonModel
from users.models import User

class ParentStudent(CommonModel):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parents')
    relationship = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'parents_parentstudent'
        verbose_name = 'parent-student relationship'
        verbose_name_plural = 'parent-student relationships'
        ordering = ["-id"]
        unique_together = ('parent', 'student')

    def __str__(self):
        return f"{self.parent} - {self.student}"
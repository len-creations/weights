from django.db import models
from datetime import date
# Create your models here.
class Exam(models.Model):
    exam_name= models.CharField(max_length=100)
    difficulty_rating = models.IntegerField()
    max_difficulty = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return self.exam_name
    
class Employee(models.Model):
    staff_number =models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    Team=models.CharField(max_length=100)
    Facility=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExamScore(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    weighted_score = models.FloatField(null=True, blank=True)
    exam_date=models.DateField(default=date.today)
    
    def save(self, *args, **kwargs):
        # Calculate weighted score as score * weight from associated exam
        self.weighted_score = self.score * self.exam.weight
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.exam.exam_name}"
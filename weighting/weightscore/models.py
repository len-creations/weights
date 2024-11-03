from django.db import models

# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=100)
    difficulty_rating = models.IntegerField()
    max_difficulty = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    staff_number = models.IntegerField()
    name = models.CharField(max_length=100)
    Team=models.CharField(max_length=100)
    Facility=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExamScore(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    weighted_score = models.FloatField()

    def __str__(self):
        return f"{self.employee.name} - {self.exam.name}"
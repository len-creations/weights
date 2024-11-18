from django.db import models
from datetime import date
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
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
    designation=models.CharField(max_length=100,default="Technician")
    Facility=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    def count_completed_trainings(self):
        """Returns the count of completed trainings employee."""
        return self.completed_trainings.filter(date_completed__isnull=False).count()

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
    
class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    code = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=20, default="EQUIPMENT MANUAL")
    file = models.FileField(upload_to='Training/uploads/', blank=True, null=True)
    facility=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_pages = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class CompletedTraining(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='completed_trainings')
    training_module = models.ForeignKey('TrainingModule', on_delete=models.CASCADE, related_name='completed_by_profiles')
    date_completed = models.DateTimeField(default=timezone.now)

    @property
    def date_of_expiry(self):
        """Return the expiry date as 2 years after the date completed."""
        return self.date_completed + timedelta(days=730) 

    class Meta:
        unique_together = ('employee', 'training_module')
        ordering = ['-date_completed']
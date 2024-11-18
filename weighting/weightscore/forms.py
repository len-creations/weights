from django import forms
from .models import TrainingModule

class UploadExamFilesForm(forms.Form):
    exam_parameters_file = forms.FileField(label="Exam Parameters File")
    
class UploademployeeFilesForm(forms.Form):
    employee_score_file=forms.FileField(label="Employee scores File")

class employeedetailsFilesForm(forms.Form):
    employee_file=forms.FileField(label="Employee detail")

class TrainingModuleForm(forms.Form):
    Training_module_file = forms.FileField(label="Training Module File")

class CompletedTrainingModuleForm(forms.Form):
    Completed_trainings_file=forms.FileField(label="Completed trainings")
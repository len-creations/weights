from django import forms
from .models import CompletedTraining, ExamScore,Employee

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

class CompletedTrainingForm(forms.ModelForm):
    employee = forms.CharField(
        required=True,
        label="Employee",
        widget=forms.TextInput(attrs={'placeholder': 'Type employee name or staff number...'})
    )

    class Meta:
        model = CompletedTraining
        fields = ['training_module', 'date_completed']
        widgets = {
            'date_completed': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_employee(self):
        employee_input = self.cleaned_data.get('employee')
        try:
            employee = Employee.objects.get(
                name__icontains=employee_input
            )  # You can expand this with other fields like staff_number
            return employee
        except Employee.DoesNotExist:
            raise forms.ValidationError("No matching employee found. Please check the input.")
        
class ExamScoreForm(forms.ModelForm):
    class Meta:
        model = ExamScore
        fields = ['employee', 'exam', 'score', 'exam_date']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
        }
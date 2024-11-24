from django import forms
from .models import CompletedTraining, ExamScore,Employee
from django.db.models import Q
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
    employee_input = forms.CharField(
        required=True,
        label="Employee",
        widget=forms.TextInput(attrs={'placeholder': 'Type employee staff number or name ...'})
    )

    class Meta:
        model = CompletedTraining
        fields = ['training_module', 'date_completed']
        widgets = {
            'date_completed': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_employee_input(self):
        employee_input = self.cleaned_data.get('employee_input').strip()
        print(f"Input received: '{employee_input}'")
        try:
            employee = Employee.objects.get(
                Q(name__iexact=employee_input) | Q(staff_number__iexact=employee_input)
            )
            return employee
        except Employee.DoesNotExist:
            print("Exact match not found, attempting partial match.")
            try:
                employee = Employee.objects.get(
                    Q(name__icontains=employee_input) | Q(staff_number__icontains=employee_input)
                )
                return employee
            except Employee.DoesNotExist:
                print("No matching employee found.")
                raise forms.ValidationError("No matching employee found. Please check the input.")
            
class ExamScoreForm(forms.ModelForm):
    class Meta:
        model = ExamScore
        fields = ['employee', 'exam', 'score', 'exam_date']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
        }
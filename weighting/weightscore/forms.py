from django import forms

class UploadExamFilesForm(forms.Form):
    exam_parameters_file = forms.FileField(label="Exam Parameters File")
    
class UploademployeeFilesForm(forms.Form):
    employee_score_file=forms.FileField(label="Employee scores File")
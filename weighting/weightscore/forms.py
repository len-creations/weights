from django import forms

class UploadExamFilesForm(forms.Form):
    exam_parameters_file = forms.FileField(label="Exam Parameters File")
    employee_scores_file = forms.FileField(label="Employee Scores File")
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadExamFilesForm
import pandas as pd
import os
from .models import Exam, Employee, ExamScore
from .forms import UploadExamFilesForm
def index(request):
    return render(request,'weightscore/upload_exam_files.html')

def upload_exam_files(request):
    if request.method == 'POST':
        form = UploadExamFilesForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Get the uploaded files
            exam_parameters_file = request.FILES['exam_parameters_file']
            employee_scores_file = request.FILES['employee_scores_file']
            
            # Save the files temporarily to process them
            exam_parameters_path = os.path.join('/tmp', exam_parameters_file.name)
            employee_scores_path = os.path.join('/tmp', employee_scores_file.name)
            
            with open(exam_parameters_path, 'wb+') as destination:
                for chunk in exam_parameters_file.chunks():
                    destination.write(chunk)

            with open(employee_scores_path, 'wb+') as destination:
                for chunk in employee_scores_file.chunks():
                    destination.write(chunk)
            
            # Process the uploaded files
            handle_exam_files(exam_parameters_path, employee_scores_path)

            return HttpResponse('Files uploaded and processed successfully.')
    else:
        form = UploadExamFilesForm()

    return render(request, 'weightscore/upload_exam_files.html', {'form': form})

def handle_exam_files(exam_parameters_path, employee_scores_path):
    """
    Handles reading the two Excel files, extracting data, and saving them into the Django database.

    :param exam_parameters_path: Path to the exam parameters Excel file.
    :param employee_scores_path: Path to the employee scores Excel file.
    """
    # --- Read the exam parameters Excel file ---
    exam_params_df = pd.read_excel(exam_parameters_path)

    # Loop through the exam parameters and save/update them in the database
    for index, row in exam_params_df.iterrows():
        exam_name = row['Exam']  # Column containing the exam names
        difficulty_rating = row['Difficulty rating (1-10)']
        max_difficulty = row['Max difficulty']
        weight = row['Weight']

        # Create or update Exam object
        exam, created = Exam.objects.update_or_create(
            name=exam_name,
            defaults={
                'difficulty_rating': difficulty_rating,
                'max_difficulty': max_difficulty,
                'weight': weight
            }
        )

    print("Exam Parameters Processed and Saved to Database")

    # --- Read the employee scores Excel file ---
    employee_scores_df = pd.read_excel(employee_scores_path)

    # Loop through the employee scores and save them into the database
    for index, row in employee_scores_df.iterrows():
        staff_number = row['Staff number']
        name = row['Employee Name']
        team = row['Team']

        # Create or update Employee object
        employee, created = Employee.objects.update_or_create(
            staff_number=staff_number,
            defaults={'name': name, 'team': team}
        )

        # Loop through the exams and save the scores
        for exam_name in ['Stacker Crane', 'EWS', 'H9TV', 'ULD & BBTV']:  # Adjust according to your exam columns
            score = row[exam_name]

            try:
                # Fetch the corresponding Exam object
                exam = Exam.objects.get(name=exam_name)

                # Calculate the weighted score based on the weight
                weighted_score = score * exam.weight

                # Create or update the ExamScore object
                ExamScore.objects.update_or_create(
                    employee=employee,
                    exam=exam,
                    defaults={'score': score, 'weighted_score': weighted_score}
                )

            except Exam.DoesNotExist:
                print(f"Exam '{exam_name}' does not exist in the database.")
                continue

    print("Employee Scores Processed and Saved to Database")
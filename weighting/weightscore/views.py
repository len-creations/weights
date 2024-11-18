from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UploadExamFilesForm,UploademployeeFilesForm,employeedetailsFilesForm,TrainingModuleForm,CompletedTrainingModuleForm
import pandas as pd
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Exam, Employee, ExamScore,CompletedTraining
from .forms import UploadExamFilesForm,TrainingModule
from django.core.paginator import Paginator
from django.db.models import Sum,Q
from operator import itemgetter
from dateutil.parser import parse
def index(request):
    return render(request,'weightscore/index.html')

def extract_param_data(request):
    if request.method == 'POST':
        form = UploadExamFilesForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['exam_parameters_file']
            df = pd.read_excel(file, sheet_name='Cargo')
            df.columns = df.columns.str.strip() 
            # Print the column names to inspect for any spaces or formatting issues
            print(df.columns)

            for _, row in df.iterrows():
                exam_name = row['Exam']
                difficulty_rating = row['Difficulty rating']
                max_difficulty = row['Max difficulty']
                weight = row['Weight']

                # Attempt to save the data
                Exam.objects.update_or_create(
                    exam_name=exam_name,
                    defaults={
                        'difficulty_rating': difficulty_rating,
                        'max_difficulty': max_difficulty,
                        'weight': weight
                    }
                )
    else:
        form = UploadExamFilesForm()
    
    return render(request, 'weightscore/addingdata.html', {'form': form})

def extract_employee_data(request):

    if request.method == 'POST':
        form = UploademployeeFilesForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['employee_score_file']
            df = pd.read_excel(file, sheet_name='Sheet1')
            df.columns = df.columns.str.strip() 
            # Print the column names to inspect for any spaces or formatting issues
            # print(df.columns)
            exam_names_in_db = Exam.objects.values_list('exam_name', flat=True)

            for _, row in df.iterrows():
                staff_number = row['Staff number']
                employee_name = row['Employee Name']
                facility = row['Facility']
                team = row['Team']
                exam_date = pd.to_datetime(row['date'], format='%d-%mmm-%yyyy').date() 

                employee, created = Employee.objects.update_or_create(
                    staff_number=staff_number,
                    defaults={'name': employee_name, 'Facility': facility, 'Team': team}
                )

                for exam_name in df.columns:
                    # Skip the non-exam columns like 'Staff number', 'Employee Name', etc.
                    if exam_name in ['Staff number', 'Employee Name', 'Facility', 'Team', 'date']:
                        continue

                    if exam_name not in exam_names_in_db:
                        continue
                    
                    score = row[exam_name]
    
                    if pd.notnull(score):  # Skip rows with missing exam scores
                        try:
                            # Assuming score is a percentage (e.g., '0.81')
                            score = float(score) * 100.0
                        except ValueError:
                            score = 0  
                        try:
                            exam = Exam.objects.get(exam_name=exam_name)
                        except Exam.DoesNotExist:
                            print(f"Exam {exam_name} not found in database!")
                            continue 
                        # Create the ExamScore object
                        print(score)
                        ExamScore.objects.update_or_create(
                            employee=employee,
                            exam=exam,
                            score=score,
                            exam_date=exam_date
                        )    
    else:
        form = UploademployeeFilesForm()
    
    return render(request, 'weightscore/addingdata.html', {'form': form})

def get_employee_data(request):

    if request.method == 'POST':
        form = employeedetailsFilesForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['employee_file']
            df = pd.read_excel(file, sheet_name='Sheet1')
            df.columns = df.columns.str.strip()
            # print(df.columns)
            for index, row in df.iterrows():
                staff_number = row['Staff number']
                name = row['Employee Name']
                team = row['Team']
                designation = row['designation']
                facility = row['Facility']

                # Check if the Employee already exists by staff_number
                employee, created = Employee.objects.get_or_create(
                    staff_number=staff_number,
                    defaults={
                        'name': name,
                        'Team': team,
                        'designation': designation,
                        'Facility': facility,
                    }
                )

                # If the Employee exists, update the data (excluding staff_number)
                if not created:
                    employee.name = name
                    employee.Team = team
                    employee.designation = designation
                    employee.Facility = facility
                    employee.save()  # Save the updated record

            # Optional: Print or log data for debugging
            print(f"Processed {len(df)} records.")

    else:
        form = employeedetailsFilesForm()

    return render(request, 'weightscore/addingdata.html', {'form': form})


def training_module_master_list(request):
    if request.method == 'POST':
        form = TrainingModuleForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['Training_module_file']
            df = pd.read_excel(file, sheet_name='Sheet1')
            df.columns = df.columns.str.strip()

            for _, row in df.iterrows():
                # Create a TrainingModule instance for each row
                module = TrainingModule(
                    title=row['Module Title'], 
                    code=row['CODE'], 
                    category=row['Category'],
                    facility=row['FACILITY'],  
                )
                module.save()

            # Now, return after processing all rows
            return render(request, 'weightscore/index.html', {'form': form, 'success': True})

        else:
            return render(request, 'weightscore/addingdata.html', {'form': form, 'error': 'Invalid form data'})

    else:
        form = TrainingModuleForm()

    return render(request, 'weightscore/addingdata.html', {'form': form})

def get_completed_trainings(request):
    if request.method == 'POST':
        form = CompletedTrainingModuleForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['Completed_trainings_file']
            df = pd.read_excel(file, sheet_name='Sheet1')
            df.columns = df.columns.str.strip()

            # Extract training module columns (columns starting with 'LSME')
            training_columns = [col for col in df.columns if col.startswith('LSME')]

            # Process each row in the DataFrame
            for _, row in df.iterrows():
                # Get the employee using 'Staff number'
                staff_number = row['Staff number']
                try:
                    employee = Employee.objects.get(staff_number=staff_number)
                except Employee.DoesNotExist:
                    # Skip if employee does not exist
                    print(f"Employee with Staff Number {staff_number} does not exist")
                    continue

                for col in training_columns:
                    date_completed = row[col]
                    print(f"Raw data in column {col} for Staff Number {staff_number}: {date_completed}")
                    if pd.isna(date_completed):  # Skip empty columns
                        print(f"Skipping column {col} for Staff Number {staff_number}: No date provided")
                        continue

                    try:
                        date_completed = parse(str(date_completed))  # Dynamically parse any valid date format
                        date_completed = make_aware(date_completed)
                    except (ValueError, TypeError):
                         print(f"Unrecognized date format in column {col} for Staff Number {staff_number}: {date_completed}")
                         continue

                    # Extract training module code (text before the slash)
                    code = col.split('/')[0]

                    # Check if the training module exists
                    try:
                        training_module = TrainingModule.objects.get(code=code)
                    except TrainingModule.DoesNotExist:
                        print(f"Training Module with Code {code} does not exist")
                        continue

                    # Debugging statement to show the record being processed
                    print(f"Saving record: Employee={employee}, Training Module={training_module}, Date={date_completed}")

                    # Update or create the completed training record
                    CompletedTraining.objects.update_or_create(
                        employee=employee,
                        training_module=training_module,
                        defaults={'date_completed': date_completed}
                    )
    else:
        form = CompletedTrainingModuleForm()

    return render(request, 'weightscore/addingdata.html', {'form': form})
def view_completed_trainings(request):
    # Get all employees and their completed training records
    completed_trainings = CompletedTraining.objects.select_related('employee', 'training_module').all()
    # Group completed trainings by employee
    employee_trainings = {}
    for training in completed_trainings:
        employee = training.employee
        if employee not in employee_trainings:
            employee_trainings[employee] = []
        employee_trainings[employee].append(training)
    employee_trainings.append({
        
    })
    # Pass the data to the template
    return render(request, 'weightscore/completed_trainings.html', {'employee_trainings': employee_trainings})

def employee_performance(request):
    filter_exam_count = request.GET.get('exam_count')
    employees = Employee.objects.all()

    performance_data = []
    for employee in employees:
        # Get the exam scores for the employee (filtering for exams with a score greater than 1)
        exam_scores = ExamScore.objects.filter(employee=employee, score__gt=1)
        
        # If a filter is provided, only consider employees with the specified number of exams
        if filter_exam_count:
            exam_count = exam_scores.count()
            if int(filter_exam_count) != exam_count:
                continue 

        # Calculate total weighted score
        total_weighted_score = exam_scores.aggregate(total_weighted_score=Sum('weighted_score'))['total_weighted_score'] or 0
        performance_data.append({
            'employee': employee,
            'exam_scores': exam_scores,
            'total_weighted_score': total_weighted_score,
        })

    # Sort the performance data by total weighted score in descending order
    performance_data = sorted(performance_data, key=itemgetter('total_weighted_score'), reverse=True)

    # Paginate the results
    paginator = Paginator(performance_data, 10)  # 10 results per page
    page = request.GET.get('page')
    performance_data = paginator.get_page(page)

    # Check if the filter is applied and render accordingly
    if filter_exam_count:
        return render(request, 'weightscore/filter.html', {
            "page_obj": performance_data,
            "filter_exam_count": filter_exam_count  
        })
    else:
        # If no filter is applied, render the index page
        return render(request, 'weightscore/index.html', {
            "page_obj": performance_data,
            "filter_exam_count": filter_exam_count  
        })

def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Search employees based on query (name, staff number, or team)
        employee_results = Employee.objects.filter(
            Q(name__icontains=query) | 
            Q(staff_number__icontains=query) | 
            Q(Team__icontains=query)
        )

        for employee in employee_results:
            # Fetch exam scores for the employee where score > 1
            exam_scores = ExamScore.objects.filter(employee=employee, score__gt=1)
            
            # Calculate total weighted score
            total_weighted_score = exam_scores.aggregate(
                total_weighted_score=Sum('weighted_score')
            )['total_weighted_score'] or 0

            # If there are no exam scores, add a default set of values
            if not exam_scores:
                exam_scores = [{
                    'exam_name': 'None',
                    'score': 0,
                    'weighted_score': 0,
                    'exam_date': 'N/A'
                }]
            
            results.append({
                'employee': employee,
                'exam_scores': exam_scores,
                'total_weighted_score': total_weighted_score
            })
        
        # Paginate the results if there are many
        paginator = Paginator(results, 10)
        page = request.GET.get('page')
        results_page = paginator.get_page(page)

        context = {
            'query': query,
            'results': results_page,
        }

    else:
        context = {
            'query': '',
            'results': results,
        }

    return render(request, 'weightscore/search.html', context)
# def employee_performance(request):
#     employees = Employee.objects.all()
#     performance_data = []
#     for employee in employees:
#            exam_scores = ExamScore.objects.filter(employee=employee, score__gt=1)
#            total_weighted_score = exam_scores.aggregate(total_weighted_score=Sum('weighted_score'))['total_weighted_score'] or 0
#            performance_data.append({
#             'employee': employee,
#             'exam_scores': exam_scores,
#             'total_weighted_score': total_weighted_score,
#         })
#     performance_data = sorted(performance_data, key=itemgetter('total_weighted_score'), reverse=True)      
#     paginator = Paginator(performance_data, 10) 
#     page = request.GET.get('page')
#     performance_data = paginator.get_page(page)
#     page_obj = paginator.get_page(page)
#     return render(request, 'weightscore/index.html', {
#          "page_obj": page_obj
#     })


       

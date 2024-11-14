from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UploadExamFilesForm,UploademployeeFilesForm
import pandas as pd
from .models import Exam, Employee, ExamScore
from .forms import UploadExamFilesForm
from django.core.paginator import Paginator
from django.db.models import Sum,Q

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

def employee_performance(request):
    employees = Employee.objects.all()
    performance_data = []
    for employee in employees:
           exam_scores = ExamScore.objects.filter(employee=employee, score__gt=1)
           total_weighted_score = exam_scores.aggregate(total_weighted_score=Sum('weighted_score'))['total_weighted_score'] or 0
           performance_data.append({
            'employee': employee,
            'exam_scores': exam_scores,
            'total_weighted_score': total_weighted_score,
        })
    paginator = Paginator(performance_data, 10) 
    page = request.GET.get('page')
    performance_data = paginator.get_page(page)
    page_obj = paginator.get_page(page)
    return render(request, 'weightscore/index.html', {
         "page_obj": page_obj
    })

def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Search employees based on query (name, staff number, or team)
        employee_results = Employee.objects.filter(
            Q(name__icontains=query) | 
            Q(staffnumber__icontains=query) | 
            Q(Team__icontains=query)
        )

        for employee in employee_results:
            # Fetch exam scores for the employee where score > 1
            exam_scores = ExamScore.objects.filter(employee=employee, score__gt=1)
            
            # Calculate total weighted score
            total_weighted_score = exam_scores.aggregate(
                total_weighted_score=Sum('weighted_score')
            )['total_weighted_score'] or 0
            
            results.append({
                'employee': employee,
                'exam_scores': exam_scores,
                'total_weighted_score': total_weighted_score
            })
        
        # Paginate the results if there are many
        paginator = Paginator(results, 10)  # 10 results per page
        page = request.GET.get('page')
        results_page = paginator.get_page(page)

        context = {
            'query': query,
            'results': results_page,  # Use paginated results
        }

    else:
        # If there's no search query, return an empty context
        context = {
            'query': '',
            'results': results,
        }

    return render(request, 'weightscore/index.html', context)
            
       


# def search(request):
#     query = request.GET.get('q')
#     results = []
#     if query:
#         # Search in Profile, TrainingModule,Exam,TrainingDocuments
#         employee_results = Employee.objects.filter(
#             Q(name__icontains=query) | 
#             Q(staffnumber__icontains=query) | 
#             Q(Team__icontains=query)
#         )
#         for employee in employee_results:
#            exam_scores = ExamScore.objects.filter(employee=employee, score__gt=1)
#            total_weighted_score = exam_scores.aggregate(total_weighted_score=Sum('weighted_score'))['total_weighted_score'] or 0
#            results.append({
#                  'employee': employee,
#                  'exam_scores': exam_scores,
#                  'total_weighted_score': total_weighted_score
#             })
#         context = {
#         'query': query,
#         'results': results,
#            }
#         return render(request, 'Training/index.html', context)

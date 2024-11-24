from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.index, name='index'),
    path('add-completed-training/', views.add_completed_training, name='add_completed_training'),
    path('add-exam-score/', views.add_exam_score, name='add_exam_score'),
    path("extract-param-data/", views.extract_param_data, name="extract_param_data"),
    path("extract-employee-data/", views.extract_employee_data, name="extract_employee_data"),
    path('employee/<int:employee_id>/', views.employee_trainings, name='employee_trainings'),
    path('employee/<int:employee_id>/trainings/', views.employee_trainings_progress, name='employee_trainings_progress'),
    path('performance/', views.employee_performance, name='employee_performance'),
    path('search/', views.search, name='search'),
    path('upload/', views.get_employee_data, name='get_employee_data'),
    path('module-list/', views.training_module_master_list, name='training_module_master_list'),
    path('completed-trainings/', views.get_completed_trainings, name='get_completed_trainings'),
    path('completed-sessions/', views.view_completed_trainings, name='view_completed_trainings'),
    # path('addfiles/', views.upload_exam_files, name='upload_exam_files'),
    # path('upload/', views.handle_exam_files, name='handle_exam_files'),
    # path('upload-exam/',views.extract_data, name='upload_exam'),

]
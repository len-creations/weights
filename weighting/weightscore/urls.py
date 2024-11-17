from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
     path('', views.index, name='index'),
     path("extract-param-data/", views.extract_param_data, name="extract_param_data"),
     path("extract-employee-data/", views.extract_employee_data, name="extract_employee_data"),
     path('performance/', views.employee_performance, name='employee_performance'),
     path('search/', views.search, name='search'),
    path('upload/', views.get_employee_data, name='get_employee_data'),
    path('module-list/', views.training_module_master_list, name='training_module_master_list'),
    # path('addfiles/', views.upload_exam_files, name='upload_exam_files'),
    # path('upload/', views.handle_exam_files, name='handle_exam_files'),
    # path('upload-exam/',views.extract_data, name='upload_exam'),

]
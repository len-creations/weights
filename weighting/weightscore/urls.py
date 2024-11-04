from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
     path("", views.index, name="index"),
    path('addfiles/', views.upload_exam_files, name='upload_exam_files'),
    path('upload/', views.handle_exam_files, name='handle_exam_files'),
    path('upload-exam/',views.extract_data, name='upload_exam'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
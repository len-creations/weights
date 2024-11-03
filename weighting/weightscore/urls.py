from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
     path("", views.index, name="index"),
    path('upload/', views.upload_exam_files, name='upload_exam_files'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
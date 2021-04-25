from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('files', views.files_view, name="files"),
    path('add/file', views.add_file, name="addFile"),
]

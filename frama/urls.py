from django.urls import path

from . import views

urlpatterns = [
    path('init', views.init, name="init"),
    path('main', views.main, name="main"),
    path('main/<str:chosen_file>', views.main, name="main"),
    path('files', views.files_view, name="files"),
    path('file/add', views.FileCreateView.as_view(), name="file-add"),
    path('file/delete', views.FileDeleteView.as_view(), name="file-delete"),
    path('user/add', views.UserCreateView.as_view(), name="user-add"),
    path('directory/add', views.DirectoryCreateView.as_view(), name="directory-add"),
    path('directory/delete', views.DirectoryDeleteView.as_view(), name="directory-delete"),
    path('file-section/add', views.FileSectionCreateView.as_view(), name="file-section-add"),
    path('tree', views.tree, name="tree"),
    path('tree/<str:chosen_file>', views.tree_highlight, name="tree-highlight"),
    path('focus/<str:chosen_file>', views.focus_on_program_elements, name="focus-file"),
]

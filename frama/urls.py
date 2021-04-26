from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('main', views.main, name="main"),
    path('main/<str:chosen_file>', views.main, name="main"),
    path('files', views.files_view, name="files"),
    path('file/add', views.FileCreateView.as_view(), name="file-add"),
    path('user/add', views.UserCreateView.as_view(), name="user-add"),
    # path('user/delete', views.UserSetInvalid.as_view(), name="user-delete"),
    path('directory/add', views.DirectoryCreateView.as_view(), name="directory-add"),
    path('file-section/add', views.FileSectionCreateView.as_view(), name="file-section-add"),
    path('tree', views.tree, name="tree"),
    path('tree/<str:chosen_file>', views.tree_highlight, name="tree-highlight"),
    path('focus/<str:chosen_file>', views.focus_on_program_elements, name="focus-file"),

    # path('add/file', views.add_file, name="addFile"),
]

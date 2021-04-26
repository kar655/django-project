from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('files', views.files_view, name="files"),
    path('file/add', views.FileCreateView.as_view(), name="file-add"),
    path('user/add', views.UserCreateView.as_view(), name="user-add"),
    # path('user/delete', views.UserSetInvalid.as_view(), name="user-delete"),
    path('directory/add', views.DirectoryCreateView.as_view(), name="directory-add"),
    path('tree', views.tree, name="tree"),
    path('tree/<str:chosen_file>', views.tree_highlight, name="tree-highlight"),

    # path('add/file', views.add_file, name="addFile"),
]

from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('tabs', views.TabsView.as_view(), name="tabs"),
    path('program-elements', views.ProgramElements.as_view(), name='program-elements'),
    path('file-content', views.FileContent.as_view(), name='file-content'),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', login_required(views.LogoutView.as_view()), name="logout"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('main', login_required(views.MainView.as_view()), name="main"),
    path('file/add', login_required(views.FileCreateView.as_view()), name="file-add"),
    path('file/delete', login_required(views.FileDeleteView.as_view()), name="file-delete"),
    path('directory/add', login_required(views.DirectoryCreateView.as_view()), name="directory-add"),
    path('directory/delete', login_required(views.DirectoryDeleteView.as_view()), name="directory-delete"),
    path('file-section/add', login_required(views.FileSectionCreateView.as_view()), name="file-section-add"),
]

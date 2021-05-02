from django.urls import path

from . import views

urlpatterns = [
    path('init', views.init, name="init"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('main', views.MainView.as_view(), name="main"),
    path('main/<str:chosen_tab>/<str:chosen_file>', views.MainView.as_view(), name="main-tab-file"),
    path('file/add', views.FileCreateView.as_view(), name="file-add"),
    path('file/delete', views.FileDeleteView.as_view(), name="file-delete"),
    path('user/add', views.UserCreateView.as_view(), name="user-add"),
    path('directory/add', views.DirectoryCreateView.as_view(), name="directory-add"),
    path('directory/delete', views.DirectoryDeleteView.as_view(), name="directory-delete"),
    path('file-section/add', views.FileSectionCreateView.as_view(), name="file-section-add"),
]

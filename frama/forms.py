from django import forms

from .models import User, File, Directory


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput()
        }


class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = "__all__"
        exclude = ["timestamp", "is_valid", "user"]


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = "__all__"
        exclude = ["timestamp", "is_valid", "user"]

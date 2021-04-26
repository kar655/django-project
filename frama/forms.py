from django import forms

from .models import User, File, Directory, FileSection


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


class DirectoryDeleteForm(forms.Form):
    directory = forms.ModelChoiceField(queryset=Directory.objects.filter(is_valid=True))


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = "__all__"
        exclude = ["timestamp", "is_valid", "user"]


class FileDeleteForm(forms.Form):
    file = forms.ModelChoiceField(queryset=File.objects.filter(is_valid=True))


class FileSectionForm(forms.ModelForm):
    class Meta:
        model = FileSection
        fields = "__all__"
        exclude = ["timestamp", "is_valid", "user"]
